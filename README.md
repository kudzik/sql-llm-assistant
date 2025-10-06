# Asystent LLM do wyszukiwania w lokalnej bazie SQLite

## Opis
Prosty asystent oparty na modelu OpenAI, który pomaga przeszukiwać lokalną bazę danych SQLite za pomocą pytań zadawanych w naturalnym języku. 
Projekt pokazuje integrację LLM z bazą danych i interaktywnego UI Gradio.

## Uruchomienie

1. Sklonuj repozytorium

```
git clone https://github.com/twojaccount/sql-llm-assistant.git
cd sql-llm-assistant
```

2. Utwórz wirtualne środowisko i zainstaluj zależności

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Ustaw zmienną środowiskową `OPENAI_API_KEY` lub wprowadź bezpośrednio w `app.py`

4. Uruchom aplikację

```
python app.py
```

5. W przeglądarce otworzy się UI Gradio do zadawania pytań.

## Przykładowe pytania

- Jakie mamy dziś promocje na elektronikę?
- Pokaż ostatnie zgłoszenia serwisowe.
- Jaki jest stan magazynowy Laptop XYZ?

---

## Struktura bazy danych

- `products`: dane o produktach, ich kategoriach, cenach itp.
- `customers`: dane klientów
- `service_requests`: zgłoszenia serwisowe powiązane z klientami i produktami

---

## Uwagi

- Baza to lokalny plik `data.db` tworzony automatycznie przy pierwszym uruchomieniu.
- Klucz API do OpenAI musisz mieć własny.
```