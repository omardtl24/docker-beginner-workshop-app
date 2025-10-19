# Docker Beginner Workshop App — FastAPI + Express + MySQL

This project is a simple full‑stack app to practice containerization and local development. It includes:
- A FastAPI backend (Python 3.7 compatible)
- A lightweight Express.js frontend (static UI + small server)
- A MySQL schema to bootstrap the database

Dockerfiles are provided for the frontend and backend, and each component can be run locally or containerized.

## Repository structure

```
backend/
  Dockerfile
  requirements.txt
  .env        # not committed; create from .env.example
  .env.example
  app/
    main.py
    database.py
    models.py
    schemas.py

frontend/
  Dockerfile
  package.json
  server.js   # Express server serving static files
  app.js      # UI logic (talks to API)
  style.css
  .env        # not committed; create from .env.example
  .env.example

db/
  schema.sql  # creates DB, user, and people table
```

## Technologies

- Backend: FastAPI, Uvicorn, SQLAlchemy, Pydantic, PyMySQL, python‑dotenv
- Frontend: Node.js (Express), dotenv
- Database: MySQL 8.x (schema provided in `db/schema.sql`)
- Containers: Docker (multi-component, each has its own Dockerfile)

## Environment configuration (.env)

Each component may have its own `.env`. Sample files are included:
- `backend/.env.example`
- `frontend/.env.example`

Copy and adjust as needed:
- Backend variables (loaded by `python-dotenv` in `database.py`):
  - `DB_HOST` (e.g., `host.docker.internal` when backend runs in Docker and DB is on the host)
  - `DB_PORT` (e.g., `3306` or `3307`)
  - `DB_USER` (default: `workshop`)
  - `DB_PASSWORD` (default: `workshoppass`)
  - `DB_NAME` (default: `workshopdb`)

- Frontend variables (loaded by `dotenv` in `server.js`):
  - `API_URL` (e.g., `http://localhost:8000`)
  - `PORT` (default frontend port `8080`)

## Running locally (no Docker)

1) Start MySQL and create schema

```bash
mysql -u root -p < db/schema.sql
```

2) Run the backend

```bash
# from project root
cp backend/.env.example backend/.env  # then edit if needed
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

3) Run the frontend

```bash
cd frontend
cp .env.example .env  # then edit API_URL if needed
npm install
npm start
# Frontend will be available at http://localhost:8080
```

## Running with Docker (optional)

Build images:

```bash
docker build -t workshop-backend ./backend
docker build -t workshop-frontend ./frontend
```

Run containers (assuming MySQL runs on your host):

```bash
# Backend: ensure backend/.env points DB_HOST to host.docker.internal (Linux requires extra setup or use your host IP)
docker run --rm \
  --env-file backend/.env \
  -p 8000:8000 \
  --name workshop-backend \
  workshop-backend

# Frontend
docker run --rm \
  --env-file frontend/.env \
  -p 8080:8080 \
  --name workshop-frontend \
  workshop-frontend
```

Notes:
- The backend Dockerfile exposes port 8000 and runs Uvicorn: `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`.
- The frontend Dockerfile exposes port 8080 and starts the Express server via `npm start`.
- If you containerize MySQL too, create a user-defined Docker network and set `DB_HOST` to the MySQL container name.

## API overview

Base URL: `http://localhost:8000`

- `POST /person/`
  - Body: `{ "name": string, "email": string, "age": number }`
  - Returns the created person. 409 if email already exists.

- `GET /people/`
  - Returns an array of people.

- `DELETE /people/`
  - Deletes all people and returns a summary.

Open CORS is enabled for demo purposes.

## Troubleshooting

- Backend logs show "DB not ready yet" during startup: verify MySQL is running and your `DB_*` vars are correct.
- When running backend in Docker against host MySQL, set `DB_HOST=host.docker.internal` (or your host IP on Linux if not available).
- Ensure ports aren’t in use: backend 8000, frontend 8080, MySQL 3306/3307.

## License

For workshop/demo use.
