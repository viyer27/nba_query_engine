NBA Query Engine (StatMuse-style) — Local Setup
A FastAPI + React project that lets you ask NBA questions and returns answers from a local PostgreSQL database. This repo is designed so anyone can clone it and run locally in minutes—either with Docker or natively.

Features
⚡ FastAPI backend with /query endpoint

🖥️ React (Vite) frontend with a simple ChatGPT-style UI

🐘 PostgreSQL with ready-to-run schema + sample seed data

🔁 One-command startup via Docker Compose

🧪 Works without any API keys (LLM optional)

Repo Layout
php
Copy
Edit
statmuse-clone/
├─ backend/
│  ├─ app/
│  │  ├─ main.py               # FastAPI app (expects /query route)
│  │  └─ ...                   # routers, models, services, etc.
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ .env.example
├─ frontend/
│  ├─ package.json
│  ├─ src/
│  ├─ Dockerfile
│  └─ .env.example
├─ db/
│  ├─ init.sql                 # schema (tables, indexes, FKs)
│  └─ seed.sql                 # tiny sample dataset (optional but recommended)
├─ docker-compose.yml
├─ .env.example                # optional top-level defaults
├─ Makefile                    # handy shortcuts (optional)
├─ README.md
└─ LICENSE
If your tree differs, update paths/commands in this README accordingly.

Prerequisites
Choose one:

Docker Desktop 4.x (recommended), or

Native: Python 3.11+, Node 18+, PostgreSQL 16+

Quick Start — Docker (Recommended)
bash
Copy
Edit
git clone <your-repo-url> statmuse-clone
cd statmuse-clone

# Copy sample envs
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Bring everything up
docker compose up --build
Frontend: http://localhost:5173

Backend (Swagger): http://localhost:8000/docs

Postgres: localhost:5432 (see envs for user/pass/db)

On first run, Postgres will execute db/init.sql (schema) and db/seed.sql (sample rows). Edit those files to match your schema/data.

Useful Docker Commands
bash
Copy
Edit
# Stop and remove containers (keep DB volume)
docker compose down

# Nuke containers + volumes (fresh DB next time)
docker compose down -v

# Rebuild images without cache
docker compose build --no-cache
Quick Start — Without Docker
1) Database
Create a PostgreSQL database and apply schema + seeds:

bash
Copy
Edit
createdb statmuse
psql -d statmuse -f db/init.sql
psql -d statmuse -f db/seed.sql   # optional
2) Backend (FastAPI)
bash
Copy
Edit
cd backend
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
# make sure DATABASE_URL points to your local Postgres
uvicorn app.main:app --reload --port 8000
Backend will be at http://localhost:8000 (docs at /docs).

3) Frontend (Vite React)
bash
Copy
Edit
cd frontend
npm ci
cp .env.example .env
# ensure VITE_API_BASE_URL=http://localhost:8000
npm run dev
Frontend will be at http://localhost:5173.

Environment Variables
Top-level .env.example (optional defaults used by compose):

ini
Copy
Edit
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=statmuse

# Compose default for backend
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/statmuse

# CORS for local dev (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Frontend -> Backend base URL
VITE_API_BASE_URL=http://localhost:8000
REACT_APP_API_BASE_URL=http://localhost:8000
backend/.env.example:

bash
Copy
Edit
# For Docker: service name "db" resolves in the network
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/statmuse

# For native (uncomment and adjust):
# DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/statmuse

CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Optional if you use an LLM step
OPENAI_API_KEY=
frontend/.env.example (Vite):

ini
Copy
Edit
VITE_API_BASE_URL=http://localhost:8000
Never commit real secrets—only commit the *.env.example files.

API Contract (Minimal)
The backend is expected to expose:

POST /query
Body:

json
Copy
Edit
{ "question": "How many points did Bradley Beal average in 2019?" }
Response (example):

json
Copy
Edit
{
  "answer": "Bradley Beal averaged 25.6 PPG in 2019-20.",
  "sources": []
}
GET /health (optional) — returns 200 OK for health checks.

Adjust this section if your actual routes/shape differ.

Database Schema (Example)
Your db/init.sql should create at least:

teams(team_id PK, full_name, nickname, city, state, year_founded)

nba_players(player_id PK, name, year_start, year_end, position, height, weight, birth_date, hall_of_fame, draft_overall, draft_info)

rs_player_stats(id PK, player_id FK→nba_players, team_id FK→teams, season, age, games_played, ... pts, ast, trb, fg_pct, three_p, three_pa, three_p_pct, ft, fta, ft_pct, league, position, ...)

A tiny db/seed.sql is included so the app returns something immediately after startup.

Seeding Your Own Data
Replace db/seed.sql with a tiny subset of your real data (e.g., 2–3 players, 2 teams, ~2 stat rows).

Keep it small so the repo stays lightweight.

In the README, link to your full dataset or scripts for fetching it (if applicable).

Development Tips
Frontend base URL comes from VITE_API_BASE_URL.

If the frontend can’t reach the backend:

Make sure backend is on port 8000 and not blocked by firewall/VPN.

Check CORS_ORIGINS in backend/.env (must include the frontend origin).

If DB connection fails:

In Docker, wait for the db container to become healthy.

Natively, confirm psql -h localhost -U <user> -d statmuse works.

If schema changes, either:

Edit db/init.sql and recreate the DB (or docker compose down -v), or

Introduce migrations (Alembic) for a smoother workflow.

Makefile (Optional)
If you included the Makefile, you can use:

bash
Copy
Edit
make up        # docker compose up --build
make down      # docker compose down -v
make dev-api   # run backend locally
make dev-ui    # run frontend locally
make fmt       # format backend (black)
Example cURL
bash
Copy
Edit
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"How many points did LeBron average in 2023?"}'
FAQ
Do I need an OpenAI key?
No. The project can run purely on your DB. If you add LLM-powered features, set OPENAI_API_KEY in backend/.env.

Can I use a different port?
Yes—change ports in docker-compose.yml and envs accordingly.

Will this deploy to the internet?
No—this README is for local use. You can add a deploy guide later (Fly.io, Render, etc.).

Contributing
PRs welcome! Please open an issue first for major changes.

License
MIT — see LICENSE.

