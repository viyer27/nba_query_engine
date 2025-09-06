# NBA Query Engine (StatMuse-Style) — Local Setup

I’ve always had a passion for NBA analytics. Not just the surface-level numbers, but the deeper, analytical context behind them. I wanted to create a project that lets people explore those stats in a more interactive, conversational way, similar to StatMuse, but fully customizable and locally hosted. The idea was to make it easy for anyone to pull up insights on players, teams, or seasons without digging through spreadsheets or multiple sites.

The process started with sourcing and cleaning historical NBA data, designing a relational schema to link players, teams, and regular season stats, and then building a FastAPI backend that could translate natural-language questions into SQL queries. On the frontend, I went for sleek, modern interface for ease of use. 

It wasn’t without its challenges. Handling ambiguous inputs required refining query parsing. Mismatched player names and inconsistent team IDs in the dataset meant I had to write custom cleaning scripts. CORS issues popped up during local development, and at one point, my backend was returning incorrect averages because of how I was pulling and grouping data. Each hurdle forced me to dig deeper by testing SQL queries directly, normalizing the dataset, and setting up clear API contacts between the backend and frontend.

![Database Schema](example_query)

---

## Data Sources
This project includes a small sample dataset for demonstration purposes. For full NBA historical data, you can import from open sources like Basketball Reference or contact me for access to my full database.

---

## Automated Data Updates (Airflow)

To keep the database current, I added an **Apache Airflow DAG** that scrapes Basketball Reference once a week and inserts new rows into the `rs_player_stats` table.

- **Schedule**: Runs every Monday at 07:00  
- **Source**: `etl/player_scrape.py` (per-game scraper built with `pandas.read_html`)  
- **DAG**: `dags/rs_player_stats_weekly.py`  
- **Target**: Postgres table `rs_player_stats` (unique on `player_id`, `Season`, `Team`)  
- **Logic**: Compares scraped rows against what’s already in the DB, and only inserts new `(player_id, Season, Team)` combinations.  

This ensures that the project’s regular season stats stay fresh without having to re-import historical data.

---


## Future Goals
In the future, I want to expand this into a full multi-sport analytics platform, adding data for leagues like the NFL, MLB, and NHL. I’m also planning to bring in interactive visuals** such as charts, shot maps, and heatmaps so users can get greater context and granularity behind the stats. Eventually, I’d like to add predictive analytics with features like player performance projections, playoff simulations, and win probability graphs — making it a tool that’s not just about looking back at numbers, but also about understanding what might happen next.

---

## Features
- FastAPI backend with `/query`
- React + Vite frontend (ChatGPT-style)
- PostgreSQL schema + sample data included
- Runs in minutes with Docker Compose or natively
- No API keys required (LLM optional)

---

## Repo Layout
```bash
backend/   # FastAPI app
frontend/  # React app
db/        # init.sql (schema) + seed.sql (sample data)
docker-compose.yml
.env.example files
```

---

## Quick Start (Docker)
```bash
git clone "https://github.com/viyer27/nba_query_engine" statmuse-clone
cd statmuse-clone

cp ".env.example" ".env"
cp "backend/.env.example" "backend/.env"
cp "frontend/.env.example" "frontend/.env"

docker compose up --build
```
Frontend → [http://localhost:5173](http://localhost:5173)  
Backend (Swagger) → [http://localhost:8000/docs](http://localhost:8000/docs)  

---

## Quick Start (No Docker)

**DB**
```bash
createdb "statmuse"
psql -d "statmuse" -f "db/init.sql"
psql -d "statmuse" -f "db/seed.sql"
```

**Backend**
```bash
cd "backend"
python -m venv .venv && source ".venv/bin/activate"
pip install -r "requirements.txt"
cp ".env.example" ".env"
uvicorn app.main:app --reload --port 8000
```

**Frontend**
```bash
cd "frontend"
npm ci
cp ".env.example" ".env"
npm run dev
```

---

## Env Vars
- `DATABASE_URL` → PostgreSQL connection string
- `CORS_ORIGINS` → frontend URLs
- `VITE_API_BASE_URL` → backend URL

---

## Database
Three main tables:
- `teams` — team info
- `nba_players` — player info
- `rs_player_stats` — season stats

`init.sql` sets up schema, `seed.sql` adds a few rows so you get instant results.

![Database Schema](ddl)

---

## API Example
```bash
curl -X POST "http://localhost:8000/query"   -H "Content-Type: application/json"   -d '{"question":"How many points did LeBron average in 2023?"}'
```
