"""Leaderboard route returning top scores.

Auto‑generated documentation to improve code clarity.
"""


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from ..database import get_db
from ..models import Attempt, User

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/")
async def top_scores(limit: int = 20, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(User.email.label("email"), func.max(Attempt.score).label("best_score"))
        .join(Attempt, Attempt.user_id == User.id)
        .where(Attempt.is_correct == True)
        .group_by(User.email)
        .order_by(desc("best_score"))
        .limit(limit)
    )
    rows = (await db.execute(stmt)).mappings().all()
    return [{"email": r["email"], "best_score": r["best_score"]} for r in rows]
