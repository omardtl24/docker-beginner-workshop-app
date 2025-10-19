# Docker Beginners Workshop — Local App (Vite + FastAPI + MySQL)

This repository contains a **frontend (Vite)** and a **backend (FastAPI, Python 3.7-compatible)** plus SQL files to create the MySQL schema locally. No Docker files are included in this version — run everything locally.

## Quick overview
- Frontend: Vite (plain JS) — form (left) / table (right)
- Backend: FastAPI pinned for Python 3.7 (fastapi<=0.95)
- Database: MySQL 8.0 (run locally)

## Steps to run locally

1. **Prepare MySQL**
   - Start your local MySQL server (8.0).
   - Execute `db/schema.sql` and optionally `db/seed.sql` to create the DB and user:
     ```bash
     mysql -u root -p < db/schema.sql
     mysql -u root -p < db/seed.sql   # optional seed
     ```

2. **Backend**
   - Copy `backend/.env.example` → `backend/.env` and edit values if needed.
   - (Optional) create and activate a Python 3.7 virtualenv.
   - Install dependencies:
     ```bash
     pip install -r backend/requirements.txt
     ```
   - Run:
     ```bash
     uvicorn app.main:app --reload --port 8000
     ```
   - The API endpoints:
     - `GET http://localhost:8000/people`
     - `POST http://localhost:8000/people`

3. **Frontend**
   - Copy `frontend/.env.example` → `frontend/.env` (leave as is or update `VITE_API_URL`)
   - Install and run:
     ```bash
     cd frontend
     npm install
     npm run dev
     ```
   - Open Vite dev server (usually `http://localhost:5173`).

## Notes
- Backend uses python-dotenv to load `backend/.env` (so `cp backend/.env.example backend/.env`).
- Keep `.env` files out of VCS (already in `.gitignore`).
