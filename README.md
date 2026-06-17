# 🧠 MnemO Backend API

An intelligent vocabulary learning assistant that automates the process of adding and memorizing new words. Instead of manually creating flashcards, users can upload an image of a textbook page. The system automatically extracts English words, translates them, and generates creative memory associations (mnemonics) to aid retention.

This project was developed to solve the tedious problem of manual flashcard creation. From a technical perspective, it demonstrates a scalable Python architecture, asynchronous task processing (data pipelines), and seamless integration with external AI services and CLI tools.

<img width="2524" height="1265" alt="image" src="https://github.com/user-attachments/assets/384115c2-e1ae-430d-a339-b10383490644" />


## 🚀 Core Features

*   **Optical Character Recognition (OCR):** Extracts raw text from images (e.g., screenshots, book pages) using the Tesseract engine.
*   **AI Mnemonic Generator:** Integrates with Large Language Models (OpenAI API) to automatically generate translations, definitions, and personalized memory associations.
*   **Spaced Repetition System (SRS):** Features a repetition engine for optimizing learning intervals for each individual word.
*   **User Management:** Authentication and authorization system.

## 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **API Framework:** FastAPI
*   **Database:** SQLite + SQLAlchemy (ORM)
*   **Frontend:** HTML, CSS, JavaScript 
*   **Integrations:** Tesseract OCR, OpenAI API

## ⚙️ How to run the project locally

This project uses Docker Compose for easy setup of the API, Database, Redis, and Celery workers.

1. **Clone the repository:**
```
  git clone https://github.com/Elenaa78/MnemO
  cd MnemO
```
2. **Set up virtual environment & install dependencies:**
```
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
  pip install -r requirements.txt
```

3. **Environment Variables:**
Create a .env file in the root directory and add your OpenAI API key:
```
  OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the Backend (FastAPI):**
```
  uvicorn main:app --reload
```

5. **Run the Frontend:**
   Simply open the index.html file in your web browser (or use an extension like Live Server in VS Code).

## 📚 API Documentation
Once the backend is running, the interactive API documentation (Swagger UI) is automatically available at:
http://127.0.0.1:8000/docs
