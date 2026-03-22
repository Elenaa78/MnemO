from pydantic import BaseModel
from datetime import datetime

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

class FlashcardResponse(BaseModel):
    id: int
    user_id: int
    english_word: str
    polish_translation: str | None = None
    definition: str | None = None
    mnemonic: str | None = None
    source: str

    class Config:
        from_attributes = True