"""SQLAlchemy ORM models for users, puzzles, attempts.

Auto‑generated documentation to improve code clarity.
"""


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    attempts = relationship("Attempt", back_populates="user", cascade="all, delete")

class Puzzle(Base):
    __tablename__ = "puzzles"
    id = Column(Integer, primary_key=True, index=True)
    size = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    initial_state = Column(Text, nullable=False)  # JSON encoded
    solution_hash = Column(String, nullable=False)
    qr_token = Column(String, unique=True, nullable=False)
    attempts = relationship("Attempt", back_populates="puzzle", cascade="all, delete")

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id", ondelete="CASCADE"))
    submitted_state = Column(Text)
    is_correct = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="attempts")
    puzzle = relationship("Puzzle", back_populates="attempts")
