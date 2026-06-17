# 🧠 MnemO Backend API

An intelligent vocabulary learning assistant that automates the process of adding and memorizing new words. Instead of manually creating flashcards, users can upload an image of a textbook page. The system automatically extracts English words, translates them, and generates creative memory associations (mnemonics) to aid retention.

This project was developed to solve the tedious problem of manual flashcard creation. From a technical perspective, it demonstrates a scalable Python architecture, asynchronous task processing (data pipelines), and seamless integration with external AI services and CLI tools.

## 🚀 Core Features

*   **Optical Character Recognition (OCR):** Extracts raw text from images (e.g., screenshots, book pages) using the Tesseract engine.
*   **AI Mnemonic Generator:** Integrates with Large Language Models (OpenAI API) to automatically generate translations, definitions, and personalized memory associations.
*   **Spaced Repetition System (SRS):** Features a custom repetition engine based on the SuperMemo-2 algorithm, optimizing learning intervals (the forgetting curve) for each individual word.
*   **Asynchronous Background Processing:** Long-running operations (image analysis, external API requests) are offloaded to Celery task queues, ensuring high responsiveness of the main API.
*   **User Management:** A complete authentication and authorization system based on JWT tokens.

## 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **API Framework:** FastAPI
*   **Database:** PostgreSQL + SQLAlchemy (ORM) + Alembic (Migrations)
*   **Task Queue:** Celery + Redis (Message Broker)
*   **Integrations:** Tesseract OCR, OpenAI API
*   **Infrastructure:** Docker & Docker Compose

## ⚙️ How to run the project locally

This project uses Docker Compose for easy setup of the API, Database, Redis, and Celery workers.

1. **Clone the repository:**
```
  git clone https://github.com/Elenaa78/MnemO
  cd MnemO
```
2. **Environment Variables:**
Create a .env file in the root directory based on the provided template and add your API keys:
```
  OPENAI_API_KEY=your_openai_api_key_here
  DATABASE_URL=postgresql://user:password@db:5432/mnemo_db
```

3. **Build and start the containers:**
```
  docker-compose up --build
```
4. **Run database migrations (Alembic):**
```
  docker-compose exec api alembic upgrade head
```

## 📚 API Documentation
Once the containers are running, the interactive API documentation (Swagger UI) is automatically available at:
http://127.0.0.1:8000/docs
