# 🤖 SQL LLM Assistant

> Inteligentny asystent do przeszukiwania baz danych SQLite za pomocą zapytań w naturalnym języku

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange.svg)](https://gradio.app)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📝 Opis

SQL LLM Assistant to nowoczesna aplikacja, która łączy siłę sztucznej inteligencji z bazami danych. Użytkownicy mogą zadawać pytania w naturalnym języku polskim, a aplikacja automatycznie generuje i wykonuje odpowiednie zapytania SQL.

### ✨ Kluczowe funkcje
- **Natural Language Processing**: Przetwarzanie zapytań w języku polskim
- **Automatyczne generowanie SQL**: Wykorzystanie GPT-4o-mini do tworzenia zapytań
- **Interaktywny interfejs**: Nowoczesny UI oparty na Gradio
- **Bezpieczeństwo**: Tylko zapytania SELECT, brak możliwości modyfikacji danych
- **Inteligentne formatowanie**: Czytelne prezentowanie wyników

## 🚀 Demo

![Demo aplikacji](docs/demo.gif)

*Przykład użycia: "Jakie mamy promocje na elektronikę?"*

## 🛠️ Technologie

- **Backend**: Python 3.8+, SQLite
- **AI/ML**: OpenAI GPT-4o-mini
- **Frontend**: Gradio
- **Inne**: python-dotenv, sqlite3

## 💾 Instalacja

### Wymagania
- Python 3.8 lub nowszy
- Klucz API OpenAI
- Git

### Kroki instalacji

1. **Sklonuj repozytorium**
```bash
git clone https://github.com/twojaccount/sql-llm-assistant.git
cd sql-llm-assistant
```

2. **Utwórz wirtualne środowisko**
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Zainstaluj zależności**
```bash
pip install -r requirements.txt
```

4. **Skonfiguruj zmienne środowiskowe**
```bash
cp .env-example .env
# Edytuj plik .env i dodaj swój klucz OpenAI API
```

5. **Uruchom aplikację**
```bash
python app.py
```

6. **Otwórz przeglądarkę**
   - Przejdź do `http://127.0.0.1:7860`
   - Zacznij zadawać pytania!

## 💬 Przykładowe zapytania

### Produkty i promocje
```
💬 "Jakie mamy promocje na elektronikę?"
💬 "Pokaż produkty droższe niż 1000 zł"
💬 "Które produkty mają mało sztuk w magazynie?"
```

### Klienci i zgłoszenia
```
💬 "Pokaż zgłoszenia wraz z danymi klientów"
💬 "Kto ma otwarte zgłoszenia?"
💬 "Ile mamy zgłoszeń w statusie 'w trakcie'?"
```

### Analityka
```
💬 "Jakie są najdroższe produkty na promocji?"
💬 "Ilu mamy klientów?"
```

## 📊 Struktura bazy danych

Aplikacja wykorzystuje lokalną bazę SQLite z trzema głównymi tabelami:

```sql
-- Produkty
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,              -- Nazwa produktu
    category TEXT,          -- Kategoria (elektronika, meble, książki)
    price REAL,             -- Cena w zł
    promotion INTEGER,      -- Promocja: 1=tak, 0=nie
    stock INTEGER           -- Stan magazynowy
);

-- Klienci
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,              -- Imię i nazwisko
    email TEXT,             -- Adres email
    phone TEXT              -- Numer telefonu
);

-- Zgłoszenia serwisowe
CREATE TABLE service_requests (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,    -- FK do customers
    product_id INTEGER,     -- FK do products
    request_date TEXT,      -- Data zgłoszenia
    status TEXT,            -- Status: otwarty/zamknięty/w trakcie
    description TEXT        -- Opis problemu
);
```

### 💾 Przykładowe dane
- **11 produktów** w 3 kategoriach (elektronika, meble, książki)
- **5 klientów** z pełnymi danymi kontaktowymi
- **6 zgłoszeń serwisowych** w różnych statusach

## 🔒 Bezpieczeństwo

- **Tylko odczyt**: Aplikacja generuje wyłącznie zapytania `SELECT`
- **Brak modyfikacji**: Zabronione operacje `INSERT`, `UPDATE`, `DELETE`, `DROP`
- **Bezpieczne API**: Klucz OpenAI przechowywany w zmiennych środowiskowych
- **Walidacja**: Sprawdzanie i filtrowanie generowanych zapytań SQL

## 🏗 Architektura

```
┌────────────────┐
│   Gradio UI    │
│  (Frontend)    │
└───────┬────────┘
        │
┌───────┴────────┐
│  Python Backend│
│   - NLP Parser │
│   - SQL Gen    │
│   - Formatter  │
└───────┬────────┘
        │
┌───────┴────────┐    ┌────────────────┐
│  SQLite DB     │    │   OpenAI API   │
│   (data.db)    │    │  (GPT-4o-mini) │
└────────────────┘    └────────────────┘
```

## 📝 Szczegóły techniczne

- **Baza danych**: SQLite (plik `data.db`, auto-generowany)
- **Model AI**: OpenAI GPT-4o-mini
- **Interface**: Gradio Web UI
- **Dane**: Automatyczne ładowanie przykładowych danych
- **Obsługa błędów**: Pełna walidacja i komunikaty

## 🧪 Testowanie

```bash
# Uruchom testy jednostkowe
python test_simple.py

# Test formatowania odpowiedzi
python test_format_only.py
```

## 📁 Struktura projektu

```
sql-llm-assistant/
├── app.py                 # Główna aplikacja
├── requirements.txt       # Zależności Python
├── .env-example          # Przykład konfiguracji
├── .gitignore            # Pliki ignorowane przez Git
├── README.md             # Dokumentacja
├── example_queries.md    # Przykładowe zapytania
├── test_*.py             # Testy jednostkowe
└── docs/                 # Dokumentacja projektu
    ├── PRD.md            # Product Requirements
    └── CHUNK.md          # Implementacja
```

## 🔧 Rozwiązywanie problemów

### Częste problemy

**Problem**: `ModuleNotFoundError: No module named 'openai'`
```bash
# Rozwiązanie
pip install -r requirements.txt
```

**Problem**: `Error code: 401 - Invalid API key`
```bash
# Sprawdź plik .env
cat .env
# Upewnij się, że klucz jest poprawny
```

**Problem**: Aplikacja nie odpowiada
```bash
# Sprawdź czy port 7860 jest wolny
lsof -i :7860
# Lub uruchom na innym porcie
python app.py --port 7861
```

### Debug mode

```python
# Dodaj na końcu app.py
if __name__ == "__main__":
    create_sample_db()
    demo = create_gradio_interface()
    demo.launch(debug=True, share=False)
```

## 👥 Autor

**Twój Profil GitHub**
- 💼 LinkedIn: [Artur Kud](https://www.linkedin.com/in/arturkud/)
- 📧 Email: kudzik@outlook.com
- 🌐 Portfolio: [https://arturkud.hashnode.dev/](https://arturkud.hashnode.dev/)

## 📜 Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](LICENSE) po szczegóły.

## 🚀 Roadmap

- [ ] Obsługa większych baz danych (PostgreSQL, MySQL)
- [ ] Eksport wyników do CSV/Excel
- [ ] Historia zapytań
- [ ] Wizualizacje danych (wykresy)
- [ ] API REST
- [ ] Docker containerization

---

<div align="center">
  <strong>🌟 Jeśli projekt Ci się podoba, zostaw gwiazdka! 🌟</strong>
</div>