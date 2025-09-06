from __future__ import annotations
import sys
from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator


sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
import pandas as pd


from etl.player_scrape import get_per_game_stats  # uses your exact logic


DEFAULT_ARGS = {
    "owner": "statmuse",
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

PG_CONN_URI = Variable.get("PG_CONN_URI", default_var="")

def _resolve_pg_uri() -> str:
    if PG_CONN_URI:
        return PG_CONN_URI
    # Fallback to Airflow Connection 
    from airflow.hooks.base import BaseHook
    conn = BaseHook.get_connection("PGSTATMUSE")
    return conn.get_uri()


with DAG(
    dag_id="rs_player_stats_weekly",
    description="Weekly refresh of player per-game stats into rs_player_stats (incremental by player_id+season+team).",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 7 * * MON",  # Mondays at 7:00AM
    catchup=False,
    max_active_runs=1,
    tags=["statmuse", "nba", "basketball-reference", "weekly"],
    doc_md="""
    ### rs_player_stats_weekly
    - Reads players from `players` table (expects columns: `player_id`, `name`).
    - Scrapes Basketball-Reference per-game stats via `etl/player_scrape.get_per_game_stats`.
    - Dedup strategy: skip rows that already exist in `rs_player_stats` by `(player_id, season, team)`.
    """,
):
    def _fetch_players(**context) -> str:
        """Read players from DB and XCom as a list of dicts: [{player_id, name}, ...]."""
        engine = create_engine(_resolve_pg_uri(), pool_pre_ping=True, future=True)
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT player_id, name
                FROM players
                WHERE player_id IS NOT NULL AND name IS NOT NULL
            """)).mappings().all()
        players = [{"player_id": r["player_id"], "name": r["name"]} for r in rows]
        context["ti"].xcom_push(key="players", value=players)
        return f"{len(players)} players queued"

    def _load_incremental(**context) -> str:
        """For each player, scrape and insert only new (player_id, season, team) rows."""
        ti = context["ti"]
        players = ti.xcom_pull(key="players") or []

        if not players:
            return "No players found."

        engine = create_engine(_resolve_pg_uri(), pool_pre_ping=True, future=True)

        # Ensure target table exists with a unique constraint (documented expectation)
        # For plausibility: we assume rs_player_stats exists and has a unique constraint:
        # UNIQUE (player_id, season, team)
        inserted_total = 0
        checked_total = 0

        with engine.begin() as conn:
            for p in players:
                pid, name = p["player_id"], p["name"]

                
                df = get_per_game_stats(pid, name)
                if df is None or df.empty:
                    continue

                
                seasons = df["Season"].dropna().astype(str).unique().tolist()
                if not seasons:
                    continue

                # Fetch existing keys for this player and these seasons (avoid full table scan)
                existing = conn.execute(
                    text("""
                        SELECT season, team
                        FROM rs_player_stats
                        WHERE player_id = :pid
                          AND season = ANY(:seasons)
                    """),
                    {"pid": pid, "seasons": seasons},
                ).mappings().all()
                existing_keys = {(r["season"], r["team"]) for r in existing}

                # Keep only rows not already present
                df["Season"] = df["Season"].astype(str)
                df["Team"] = df["Team"].astype(str)
                new_rows = df[~df.apply(lambda r: (r["Season"], r["Team"]) in existing_keys, axis=1)].copy()

                checked_total += len(df)
                if new_rows.empty:
                    continue

                # Prepare records; align column names to snake_case minimal set for target
                
                records = new_rows.to_dict(orient="records")

                
                cols = list(new_rows.columns)
                table_cols_csv = ", ".join([f'"{c}"' for c in cols])
                values_placeholder = ", ".join([f":{c}" for c in cols])

                # If the unique constraint is named `uq_rs_player_stats_player_season_team`, we can use that.
                # Otherwise, target the natural key via a constraint or index on (player_id, season, team).
                # We'll use ON CONFLICT (player_id, season, team) DO NOTHING for readability.
                stmt = text(f"""
                    INSERT INTO rs_player_stats ({table_cols_csv})
                    VALUES ({values_placeholder})
                    ON CONFLICT (player_id, season, team) DO NOTHING
                """)
                conn.execute(stmt, records)
                inserted_total += len(records)

        return f"Checked {checked_total} rows; inserted {inserted_total} new rows."

    t_fetch_players = PythonOperator(
        task_id="fetch_players",
        python_callable=_fetch_players,
    )

    t_load_incremental = PythonOperator(
        task_id="scrape_and_upsert_incremental",
        python_callable=_load_incremental,
    )

    t_fetch_players >> t_load_incremental
