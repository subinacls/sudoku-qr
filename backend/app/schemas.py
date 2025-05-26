
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class PuzzleCreate(BaseModel):
    size: int
    difficulty: str

class PuzzleRead(BaseModel):
    id: int
    size: int
    difficulty: str
    initial_state: str
    qr_token: str
    class Config:
        orm_mode = True

class AttemptCreate(BaseModel):
    puzzle_id: int
    submitted_state: str

class AttemptRead(BaseModel):
    id: int
    puzzle_id: int
    is_correct: bool
    score: int
    class Config:
        orm_mode = True
