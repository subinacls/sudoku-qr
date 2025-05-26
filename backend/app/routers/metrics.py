"""Prometheus metrics endpoint, optionally API‑key protected.

Auto‑generated documentation to improve code clarity.
"""


from fastapi import APIRouter, Header, HTTPException, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import os

router = APIRouter()

METRICS_KEY = os.getenv("METRICS_API_KEY")

@router.get("/metrics")
async def metrics(x_api_key: str | None = Header(None)):
    if METRICS_KEY and x_api_key != METRICS_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
