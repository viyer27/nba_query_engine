
def get_per_game_stats(player_id: str, name: str) -> pd.DataFrame | None:
    url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html"
    try:
        tables = pd.read_html(url)
        per_game_df = None

        for df in tables:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(1)
            if "Season" in df.columns and "PTS" in df.columns:
                per_game_df = df
                break

        if per_game_df is None:
            print(f"{name}  Table not found")
            return None

        per_game_df = per_game_df.copy()
        per_game_df["Season"] = per_game_df["Season"].astype(str)
        per_game_df["Team"] = per_game_df["Team"].astype(str)
        per_game_df.dropna(how="all", inplace=True)
        per_game_df = per_game_df[~per_game_df["Season"].str.contains(r"\(\d+ Yrs\)", na=False)].copy()

        non_summary = per_game_df[~per_game_df["Season"].str.contains("Career|Yrs", na=False)].copy()
        duplicate_seasons = non_summary[non_summary.duplicated("Season", keep=False)]

        rows_to_drop = []
        for season in duplicate_seasons["Season"].unique():
            season_rows = per_game_df[per_game_df["Season"] == season]
            if any(season_rows["Team"].str.contains(r"TOT|\d+TM", na=False)):
                drop_rows = season_rows[~season_rows["Team"].str.contains(r"TOT|\d+TM", na=False)].index
                rows_to_drop.extend(drop_rows)

        per_game_df = per_game_df.drop(index=rows_to_drop)

        for col in per_game_df.columns:
            if col not in ["Season", "Team", "Lg", "Pos", "Awards"]:
                per_game_df.loc[:, col] = pd.to_numeric(per_game_df[col], errors="coerce")

        per_game_df.insert(0, "player_id", player_id)
        per_game_df.insert(1, "Name", name)
        per_game_df.reset_index(drop=True, inplace=True)
        print(f"{name} is good")
        return per_game_df

    except Exception as e:
        print(f"{name}  Failed: {e}")
        return None
