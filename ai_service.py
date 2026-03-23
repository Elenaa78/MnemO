import os
import json
import google.generativeai as genai
import PIL.Image
import io
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_USE_G2P"] = "1" 

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def process_image_to_flashcards(image_bytes: bytes):
    model = genai.GenerativeModel('gemini-2.5-flash')
    img = PIL.Image.open(io.BytesIO(image_bytes))
    
    prompt = """
    Przeanalizuj to zdjęcie i znajdź wszystkie angielskie słówka lub zwroty.
    Zwróć odpowiedź WYŁĄCZNIE jako czysty JSON (lista obiektów), bez znaczników markdown, według tego schematu:
    [{"english_word": "...", "polish_translation": "...", "definition": "...", "mnemonic": "..."}]

    !!! ZASADY FILTROWANIA (CZEGO NIE DODAWAĆ) !!!
    - Bezwzględnie ignoruj nagłówki, tytuły działów i sekcji (np. "VOCABULARY 1", "KEY WORDS", "UNIT 5").
    - Ignoruj polecenia dla ucznia, numery stron, przypisy i teksty organizacyjne.
    - Wyciągaj TYLKO faktyczne słówka i zwroty (zazwyczaj wypisane w listach lub kolumnach), które uczeń musi przyswoić.

    BARDZO WAŻNE - ZASADY:
    - polish_translation: Common meaning.
    - definition: Simple English (max 8 words).
    - mnemonic: A very short "sounds-like" association. 
      Format: [English word] sounds like [Polish or English word]. 
      Example: 'Curtain' sounds like 'Kurtyna'.
      Example: 'Dormitory' sounds like 'Door'.
      NO LONG STORIES. Max 15 words.
  
    """
    
    response = model.generate_content([prompt, img])
    
    clean_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_text)


def generate_flashcard_data(word: str) -> dict:
    model = genai.GenerativeModel(model_name='gemini-2.5-flash')

    prompt = f"""
    Create a simple flashcard for: "{word}".
    
    Requirements:
    - polish_translation: Common meaning.
    - definition: Simple English (max 8 words).
    - mnemonic: A very short "sounds-like" association. 
      Format: [English word] sounds like [Polish or English word]. 
      Example: 'Curtain' sounds like 'Kurtyna'.
      Example: 'Dormitory' sounds like 'Door'.
      NO LONG STORIES. Max 15 words.
    
    Return JSON:
    {{
      "polish_translation": "...",
      "definition": "...",
      "mnemonic": "..."
    }}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(text)
    except Exception as e:
        print(f"BŁĄD: {e}")
        raise e