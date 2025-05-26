"""FastAPI routes for submitting puzzle attempts and photos.

Auto‑generated documentation to improve code clarity.
"""


from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json, hashlib, math

from ..database import get_db
from ..auth import get_current_user
from .. import models, schemas, ocr

router = APIRouter(prefix="/submit", tags=["submit"])

@router.post("/attempt", response_model=schemas.AttemptRead)
async def submit_attempt(attempt: schemas.AttemptCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.execute(select(models.Puzzle).where(models.Puzzle.id == attempt.puzzle_id))
    puzzle = res.scalars().first()
    if not puzzle:
        raise HTTPException(status_code=404)
    submitted_hash = hashlib.sha256(attempt.submitted_state.encode()).hexdigest()
    correct = submitted_hash == puzzle.solution_hash
    score = 1000 if correct else 0
    attempt_obj = models.Attempt(user_id=user.id, puzzle_id=puzzle.id,
                                 submitted_state=attempt.submitted_state,
                                 is_correct=correct, score=score)
    db.add(attempt_obj)
    await db.commit()
    await db.refresh(attempt_obj)
    return attempt_obj

@router.post("/photo/{qr_token}", response_model=schemas.AttemptRead)
async def submit_photo(qr_token: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    img_bytes = await file.read()
    # verify QR matches token
    token_in_image = ocr.decode_qr(img_bytes)
    if token_in_image != qr_token:
        raise HTTPException(status_code=400, detail="QR token mismatch")
    # TODO: OCR sudoku grid to reconstruct board - placeholder
    detected_board, confidences = ocr.predict_digits_grid(img_bytes, size=puzzle.size)

if all(val==0 for row in detected_board for val in row):
    raise HTTPException(422, detail="Unable to detect grid")

    submitted_state = json.dumps(detected_board)
    res = await db.execute(select(models.Puzzle).where(models.Puzzle.qr_token == qr_token))
    puzzle = res.scalars().first()
    if not puzzle:
        raise HTTPException(status_code=404)
    submitted_hash = hashlib.sha256(submitted_state.encode()).hexdigest()
    correct = submitted_hash == puzzle.solution_hash
    score = 1000 if correct else 0
    attempt_obj = models.Attempt(user_id=None, puzzle_id=puzzle.id,
                                 submitted_state=submitted_state,
                                 is_correct=correct, score=score)
    db.add(attempt_obj)
    await db.commit()
    await db.refresh(attempt_obj)
    return attempt_obj