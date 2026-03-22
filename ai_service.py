import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_USE_G2P"] = "1" 

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

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