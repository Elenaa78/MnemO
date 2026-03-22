from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Mnemo API",
    description = "Backend dla inteligentnej aplikacji do nauki słówek z AI oraz OCR",
    version = "0.1.0"
)

@app.get("/")
def root():
    return {"message": "Witaj w Mnemo API! Wszystko działa jak należy."}

@app.get("/ping")
def ping():
    return {"status": "Ok", "pong": True}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=404, detail="Ten email jest już zajęty!")
    
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
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")
    
    new_flashcard = models.Flashcard(
        english_word=flashcard.english_word,
        user_id=user_id
    )
    db.add(new_flashcard)
    db.commit()
    db.refresh(new_flashcard)

    return new_flashcard