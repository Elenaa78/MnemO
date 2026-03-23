from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models, database, ai_service, schemas

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
        category=flashcard.category,
        source="manual",
        user_id=user_id
    )
    db.add(new_flashcard)
    db.commit()
    db.refresh(new_flashcard)
    return new_flashcard

@app.get("/flashcards/", response_model=List[schemas.FlashcardResponse])
def read_flashcards(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Flashcard)
    if category:
        query = query.filter(models.Flashcard.category == category)
    return query.all()

@app.delete("/flashcards/{flashcard_id}")
def delete_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    db_flashcard = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    if not db_flashcard: raise HTTPException(status_code=404, detail="Not found")
    db.delete(db_flashcard)
    db.commit()
    return {"message": "Usunięto"}

@app.post("/users/{user_id}/ocr/", response_model=List[schemas.FlashcardResponse])
async def upload_ocr_image(user_id: int, file: UploadFile = File(...), category: str = Form("Ogólne"), db: Session = Depends(get_db)):
    contents = await file.read()
    
    try:
        flashcards_data = ai_service.process_image_to_flashcards(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd analizy zdjęcia: {str(e)}")

    created_cards = []
    
    for item in flashcards_data:
        new_card = models.Flashcard(
            english_word=item["english_word"],
            polish_translation=item["polish_translation"],
            definition=item["definition"],
            mnemonic=item["mnemonic"],
            category=category,
            source="ocr",
            user_id=user_id
        )
        db.add(new_card)
        created_cards.append(new_card)
    
    db.commit()
    
    for card in created_cards:
        db.refresh(card)
        
    return created_cards

@app.patch("/flashcards/{flashcard_id}", response_model=schemas.FlashcardResponse)
def update_flashcard(flashcard_id: int, flashcard_update: schemas.FlashcardUpdate, db: Session = Depends(get_db)):
    db_flashcard = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="Nie znaleziono fiszki")

    update_data = flashcard_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flashcard, key, value)

    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard