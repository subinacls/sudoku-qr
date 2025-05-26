"""FastAPI routes for puzzle generation and retrieval.

Auto‑generated documentation to improve code clarity.
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json, uuid

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas, sudoku

router = APIRouter(prefix="/puzzles", tags=["puzzles"])

@router.post("/generate", response_model=schemas.PuzzleRead)

ALLOWED_SIZES = {3,6,9,12,16}
if req.size not in ALLOWED_SIZES:
    raise HTTPException(422, detail="Unsupported size")

async def generate(req: schemas.PuzzleCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    puzzle_board, solution_hash = sudoku.generate_puzzle(req.size, req.difficulty)
    qr_token = str(uuid.uuid4())
    new_puzzle = models.Puzzle(
        size=req.size,
        difficulty=req.difficulty,
        initial_state=json.dumps(puzzle_board),
        solution_hash=solution_hash,
        qr_token=qr_token
    )
    db.add(new_puzzle)
    await db.commit()
    await db.refresh(new_puzzle)
    return new_puzzle

@router.get("/{puzzle_id}", response_model=schemas.PuzzleRead)
async def get_puzzle(puzzle_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.execute(select(models.Puzzle).where(models.Puzzle.id == puzzle_id))
    puzzle = res.scalars().first()
    if not puzzle:
        raise HTTPException(status_code=404)
    return puzzle
