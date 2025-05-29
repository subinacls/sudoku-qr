from .config import cors_settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, leaderboard, metrics, pdf, puzzles, submit

from monitoring import MetricsMiddleware
app = FastAPI(title="Sudoku QR API")
app.add_middleware(MetricsMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(puzzles.router)
app.include_router(submit.router)
app.include_router(leaderboard.router)
app.include_router(metrics.router)
app.include_router(pdf.router)
