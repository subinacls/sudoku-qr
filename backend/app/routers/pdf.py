"""Route to generate printable PDF version of puzzles.

Auto‑generated documentation to improve code clarity.
"""


import io, json, base64
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from ..database import get_db
from ..models import Puzzle
from ..qr_utils import qr_to_base64

router = APIRouter(prefix="/pdf/token", tags=["pdf"])

@router.get("/{qr_token}")
async def generate_pdf(qr_token: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Puzzle).where(Puzzle.qr_token == qr_token))
    puzzle = result.scalars().first()
    if not puzzle:
        raise HTTPException(404, "Puzzle not found")

    puzzle_grid = json.loads(puzzle.initial_state)
    size = puzzle.size

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 20 * mm
    grid_size = min(width, height) - 2 * margin
    cell = grid_size / size

    # Draw outer grid
    for i in range(size + 1):
        line_w = 2 if i % int(size ** 0.5) == 0 else 1
        c.setLineWidth(line_w)
        c.line(margin, margin + i * cell, margin + grid_size, margin + i * cell)
        c.line(margin + i * cell, margin, margin + i * cell, margin + grid_size)

    # Pre‑filled numbers
    c.setFont("Helvetica", 10)
    for r, row in enumerate(puzzle_grid):
        for cidx, num in enumerate(row):
            if num != 0:
                x = margin + cidx * cell + cell * 0.35
                y = margin + grid_size - (r + 1) * cell + cell * 0.25
                c.drawString(x, y, str(num))

    # QR code
    qr_b64 = qr_to_base64(puzzle.qr_token)
    qr_bytes = base64.b64decode(qr_b64)
    qr_img = ImageReader(io.BytesIO(qr_bytes))
    qr_size = 35 * mm
    c.drawImage(qr_img, width - margin - qr_size, margin, qr_size, qr_size)
    c.setFont("Helvetica", 8)
    c.drawString(width - margin - qr_size, margin + qr_size + 5,
                 f"Upload photo at /submit-photo/{puzzle.qr_token}")

    c.showPage()
    c.save()
    buffer.seek(0)
    filename = f"puzzle_{puzzle.id}.pdf"
    return FileResponse(buffer, filename=filename, media_type="application/pdf")
