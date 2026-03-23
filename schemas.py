from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class FlashcardCreate(BaseModel):
    english_word: str
    category: str | None = "Ogólne"

class FlashcardUpdate(BaseModel):
    english_word: str | None = None
    polish_translation: str | None = None
    definition: str | None = None
    mnemonic: str | None = None
    category: str | None = None
    proficiency: int | None = None

class FlashcardResponse(BaseModel):
    id: int
    user_id: int
    english_word: str
    category: str | None = "Ogólne"
    polish_translation: str | None = None
    definition: str | None = None
    mnemonic: str | None = None
    source: str
    proficiency: int = 0

    class Config:
        from_attributes = True