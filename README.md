
# Sudoku QR Platform

This repository contains a full-stack Sudoku puzzle platform that lets users solve puzzles of various sizes
and difficulties, then submit their solutions via QR codes or photo uploads.

## Features
- **Puzzle sizes**: 3x3, 6x6, 9x9, 12x12, 16x16
- **Difficulties**: Easy, Medium, Hard, Expert
- **FastAPI backend** with PostgreSQL for scores and authentication
- **QR code workflow** for score submission and puzzle validation
- **OCR photo submission** supporting cropped image upload
- **Vite + React + Tailwind** frontend with login/register, leaderboard, verify, and photo submission views
- **Docker Compose** for local development
- **GitHub Actions** CI pipeline and Railway deployment readiness
- **Monitoring suggestions** (Prometheus/Grafana) and Sentry hooks for frontend error tracking

## Quick Start

```bash
docker compose up --build
# Backend available at http://localhost:8000
# Frontend available at http://localhost:5173
```

## Deployment to Railway
1. Fork this repo and connect it to a new Railway project.
2. Add a PostgreSQL plugin and note the `DATABASE_URL`.
3. Set environment variables for the backend service (`DATABASE_URL`, `SECRET_KEY`).
4. Deploy backend and then frontend services.

## PDF Template
The PDF generation logic should embed the QR for each puzzle and inform users they can also upload a
photo of their solved grid at `/submit-photo/<QR>`.

## OCR Cloud Function
`backend/app/ocr.py` can be deployed as a Railway Function to offload heavy OCR tasks.


## Configuration

The backend reads configuration from **environment variables** (or a local `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://sudoku:sudoku@db:5432/sudoku` | PostgreSQL connection string |
| `SECRET_KEY` | — | JWT signing key (**set in prod**) |
| `CORS_ALLOWED_ORIGINS` | `*` | Comma‑separated list of origins for CORS |
| `METRICS_API_KEY` | *(unset)* | If set, `/metrics` requires `X‑API‑Key` header |

## API Overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/auth/register` | Create account |
| `POST` | `/auth/token` | Obtain JWT |
| `POST` | `/puzzles/generate` | Generate new puzzle |
| `GET`  | `/puzzles/{id}` | Retrieve puzzle by ID |
| `GET`  | `/pdf/token/{qr_token}` | Download PDF sheet for puzzle |
| `POST` | `/submit/attempt` | Submit solution JSON |
| `POST` | `/submit/photo/{qr_token}` | Submit cropped photo |
| `GET`  | `/leaderboard/` | Top scores |
| `GET`  | `/metrics` | Prometheus metrics (*API‑key protected*) |

## Local Development

1. Copy `.env.example` → `.env` and adjust values.  
2. `docker compose up --build`  
3. API docs at `http://localhost:8000/docs`

## Production Notes

* **Set `SECRET_KEY` and `METRICS_API_KEY`.**  
* Constrain `CORS_ALLOWED_ORIGINS`.  
* Use Railway variables UI to set env values.  
* Add a PostgreSQL volume, Grafana volume, and enable TLS at the ingress.
