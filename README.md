# Asystent LLM do wyszukiwania w lokalnej bazie SQLite

## Opis
Prosty asystent oparty na modelu OpenAI GPT-4o-mini, który pomaga przeszukiwać lokalną bazę danych SQLite za pomocą pytań zadawanych w naturalnym języku. 
Projekt pokazuje integrację LLM z bazą danych i interaktywnego UI Gradio.

## Wymagania
- Python 3.8+
- Klucz API OpenAI

## Uruchomienie

1. Sklonuj repozytorium
```bash
git clone https://github.com/twojaccount/sql-llm-assistant.git
cd sql-llm-assistant
```

2. Utwórz wirtualne środowisko i zainstaluj zależności
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Skonfiguruj klucz API OpenAI
```bash
# Skopiuj plik .env-example do .env
cp .env-example .env
# Edytuj .env i wstaw swój klucz API
```

4. Uruchom aplikację
```bash
python app.py
```

5. Otwórz przeglądarkę pod adresem wyświetlonym w terminalu (zazwyczaj http://127.0.0.1:7860)

## Przykładowe pytania

- Jakie mamy dziś promocje na elektronikę?
- Pokaż ostatnie zgłoszenia serwisowe
- Jaki jest stan magazynowy Laptop XYZ?
- Ile mamy produktów w kategorii elektronika?
- Pokaż klientów z otwartymi zgłoszeniami

## Struktura bazy danych

Baza danych zawiera trzy główne tabele:

### `products`
- `id` - unikalny identyfikator produktu
- `name` - nazwa produktu
- `category` - kategoria produktu
- `price` - cena produktu
- `promotion` - czy produkt jest na promocji (1/0)
- `stock` - ilość w magazynie

### `customers`
- `id` - unikalny identyfikator klienta
- `name` - imię i nazwisko
- `email` - adres email
- `phone` - numer telefonu

### `service_requests`
- `id` - unikalny identyfikator zgłoszenia
- `customer_id` - ID klienta (klucz obcy)
- `product_id` - ID produktu (klucz obcy)
- `request_date` - data zgłoszenia
- `status` - status zgłoszenia
- `description` - opis problemu

## Bezpieczeństwo

- Aplikacja generuje tylko zapytania SELECT
- Brak możliwości modyfikacji danych (INSERT, UPDATE, DELETE)
- Klucz API przechowywany w zmiennych środowiskowych

## Uwagi techniczne

- Baza danych: lokalny plik `data.db` (tworzony automatycznie)
- Model AI: OpenAI GPT-4o-mini
- Interface: Gradio web UI
- Przykładowe dane ładowane automatycznie przy pierwszym uruchomieniu
```