from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, database, ai_service, schemas
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Mnemo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Witaj w Mnemo API! Wszystko działa jak należy."}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Ten email jest już zajęty!")
    
    fake_hashed_pass = user.password + "notreallyhashed"

    new_user = models.User(
        email=user.email,
        hashed_pass=fake_hashed_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/users/{user_id}/flashcards/", response_model=schemas.FlashcardResponse)
def create_flashcard(user_id: int, flashcard: schemas.FlashcardCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")

    ai_data = ai_service.generate_flashcard_data(flashcard.english_word)
    
    new_flashcard = models.Flashcard(
        english_word=flashcard.english_word,
        polish_translation=ai_data.get("polish_translation"),
        definition=ai_data.get("definition"),
        mnemonic=ai_data.get("mnemonic"),
        user_id=user_id
    )
    db.add(new_flashcard)
    db.commit()
    db.refresh(new_flashcard)
    return new_flashcard

@app.get("/flashcards/")
def read_flashcards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flashcards = db.query(models.Flashcard).offset(skip).limit(limit).all()
    return flashcards

@app.delete("/flashcards/{flashcard_id}")
def delete_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    db_flashcard = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Fiszka nie istnieje")
    
    db.delete(db_flashcard)
    db.commit()
    return {"message": f"Fiszka o ID {flashcard_id} została usunięta"}