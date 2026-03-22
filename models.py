from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False, unique=True)
    hashed_pass = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    flashcards = relationship("Flashcard", back_populates="owner", cascade="all, delete-orphan")


class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    english_word = Column(String, index=True, nullable=False)
    polish_translation = Column(String)
    definition = Column(Text)
    mnemonic = Column(Text)
    source = Column(String, default="manual")

    owner = relationship("User", back_populates="flashcards")
    srs_data = relationship("SRSProgress", back_populates="flashcard", uselist=False, cascade="all, delete-orphan")


class SRSProgress(Base):
    __tablename__ = "srs_progress"

    id = Column(Integer, primary_key=True, index=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"), nullable=False, unique=True)
    next_review_date = Column(DateTime, default=datetime.utcnow, index=True)
    repetition_count = Column(Integer, default=0)
    easiness_factor = Column(Float, default=2.5)

    flashcard = relationship("Flashcard", back_populates="srs_data")