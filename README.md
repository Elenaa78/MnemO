# 🧠 MnemO Backend API

Inteligentny asystent nauki słówek, który automatyzuje proces dodawania i zapamiętywania nowego słownictwa. Zamiast ręcznie wpisywać fiszki, użytkownik przesyła zdjęcie strony z podręcznika, a system samodzielnie wyciąga angielskie słowa, tłumaczy je i tworzy kreatywne skojarzenia (mnemotechniki) ułatwiające zapamiętywanie.

Projekt został stworzony, aby rozwiązać realny problem żmudnego tworzenia fiszek. Od strony technicznej ma na celu demonstrację skalowalnej architektury w Pythonie, asynchronicznego przetwarzania zadań (data pipelines) oraz integracji z zewnętrznymi usługami AI i narzędziami CLI.

## 🚀 Główne funkcjonalności

* **Optyczne Rozpoznawanie Znaków (OCR):** Ekstrakcja surowego tekstu ze zdjęć (np. zrzutów ekranu, zdjęć książek) przy użyciu silnika Tesseract.
* **AI Mnemonic Generator:** Integracja z modelem językowym (OpenAI API) do automatycznego generowania tłumaczeń, definicji i spersonalizowanych skojarzeń pamięciowych.
* **Spaced Repetition System (SRS):** Autorski silnik powtórek bazujący na algorytmie SuperMemo-2, optymalizujący interwały nauki (krzywą zapominania) dla każdego słówka indywidualnie.
* **Asynchroniczne przetwarzanie w tle:** Długotrwałe operacje (analiza obrazu, zapytania do zewnętrznych API) są oddelegowane do kolejek Celery, co gwarantuje wysoką responsywność głównego API.
* **Zarządzanie użytkownikami:** Kompletny system autoryzacji i autentykacji bazujący na tokenach JWT.

## 🛠️ Stack Technologiczny

* **Język:** Python 3.10+
* **Framework API:** FastAPI
* **Baza Danych:** PostgreSQL + SQLAlchemy (ORM) + Alembic (Migracje)
* **Kolejkowanie Zadań:** Celery + Redis (Message Broker)
* **Integracje:** Tesseract OCR, OpenAI API
* **Infrastruktura:** Docker & Docker Compose
