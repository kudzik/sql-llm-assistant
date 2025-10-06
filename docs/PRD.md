Poniżej przygotowałem dokument PRD (Product Requirements Document) oraz zestaw wymagań i danych potrzebnych do napisania prostego asystenta LLM do szybkiego wyszukiwania i raportowania danych z lokalnej bazy SQLite. Projekt będzie gotowy do uruchomienia po sklonowaniu, bez dodatkowych konfiguracji.

***

## Product Requirements Document (PRD)

### Tytuł projektu
Asystent LLM do szybkiego wyszukiwania i raportowania danych z bazy SQLite

### Cel
Umożliwić użytkownikowi zadawanie pytań w naturalnym języku dotyczących katalogu produktów, klientów lub zgłoszeń serwisowych i otrzymywanie odpowiedzi na podstawie danych zapisanych lokalnie w bazie SQLite, bez konieczności znajomości SQL.

### Problem biznesowy
Wiele małych firm i zespołów ma dane w prostych bazach (np. SQLite), a dostęp do nich wymaga umiejętności pisania zapytań SQL lub korzystania z dedykowanego oprogramowania. Asystent pozwoli na szybką ekstrakcję danych za pomocą naturalnej rozmowy, ułatwiając realne wsparcie biznesowe.

### Główne funkcje
- Integracja LLM z lokalną bazą SQLite
- Przetwarzanie zapytań użytkownika na zapytania SQL
- Wykonywanie zapytań na lokalnej bazie i pobieranie wyników
- Generowanie czytelnych raportów i odpowiedzi tekstowych na podstawie wyników zapytań
- Minimalne wymagania instalacyjne (bazuje na Pythonie i lokalnej bazie SQLite)

### Technologia
- Python 3.x
- SQLite (plik lokalny)
- OpenAI API lub inne LLM (np. integracja z Cursor AI)
- Framework do interakcji (CLI lub prosty web UI Gradio)

### Wymagania niefunkcjonalne
- Gotowość do uruchomienia po sklonowaniu repozytorium (minimalne zależności)
- Dokumentacja uruchomienia i przykładowe dane w bazie
- Przykładowe pytania i odpowiedzi w dokumentacji

***

## Wymagane dane i komponenty

### 1. Lokalna baza SQLite
- Plik `data.db` zawierający tabele:
  - `products`: id, name, category, price, promotion (bool), stock
  - `customers`: id, name, email, phone
  - `service_requests`: id, customer_id, product_id, request_date, status, description

Przykładowa zawartość, np.:
| id | name          | category    | price | promotion | stock |
|----|---------------|-------------|-------|-----------|-------|
| 1  | Laptop XYZ    | elektronika | 3000  | 1         | 15    |
| 2  | Telefon ABC   | elektronika | 1200  | 0         | 30    |

### 2. Funkcja generująca SQL na podstawie zapytania tekstowego (LLM)
- Wejście: pytanie użytkownika (tekst)
- Wyjście: zapytanie SQL (bezpieczne, zoptymalizowane)

### 3. Funkcja wykonująca zapytanie SQL na bazie SQLite
- Wejście: zapytanie SQL
- Wyjście: wyniki (lista rekordów)

### 4. Funkcja generująca czytelny raport / odpowiedź w języku naturalnym
- Wejście: wyniki zapytania SQL
- Wyjście: podsumowanie w naturalnym języku

***

## Przykładowy scenariusz użytkowania

1. Użytkownik wpisuje w interfejsie:  "Jakie mamy dziś promocje na elektronikę?"
2. LLM analizuje pytanie i generuje zapytanie SQL np.: 
```sql
SELECT name, price FROM products WHERE category='elektronika' AND promotion=1;
```
3. System wykonuje zapytanie na lokalnej bazie SQLite i zwraca dane.
4. LLM generuje odpowiedź tekstową, np.:
[translate:] "Obecnie na promocji są Laptop XYZ w cenie 3000 zł."
5. Użytkownik może zadawać kolejne pytania, np. o stan magazynowy czy status zgłoszeń serwisowych.

***

## Przygotowanie do developmentu z Cursor AI

- Przygotować lokalną bazę SQLite z przykładowymi danymi
- Napisać funkcję wrapper do wywołań OpenAI / Cursor AI, która będzie:
  - przyjmować zapytania
  - generować SQL
- Napisać funkcję do wykonania SQL na lokalnej bazie
- Napisać moduł generujący odpowiedzi raportowe
- Stworzyć prosty interfejs (np. w Gradio lub Streamlit)

***

