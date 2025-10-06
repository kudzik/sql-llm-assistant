# 📋 Changelog

Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planowane
- Obsługa PostgreSQL i MySQL
- Eksport wyników do CSV/Excel
- Historia zapytań
- Wizualizacje danych

## [1.0.0] - 2025-01-20

### Added
- 🎉 Pierwsza wersja SQL LLM Assistant
- 🤖 Integracja z OpenAI GPT-4o-mini
- 🎨 Interfejs użytkownika Gradio
- 🗄️ Lokalna baza SQLite z przykładowymi danymi
- 🔒 Bezpieczne zapytania (tylko SELECT)
- 📝 Przetwarzanie języka naturalnego (polski)
- ✨ Inteligentne formatowanie odpowiedzi
- 🧪 Testy jednostkowe
- 📚 Kompletna dokumentacja
- 🔧 Konfiguracja przez zmienne środowiskowe

### Database Schema
- `products` - 11 przykładowych produktów w 3 kategoriach
- `customers` - 5 klientów z pełnymi danymi
- `service_requests` - 6 zgłoszeń serwisowych

### Features
- Natural Language Processing dla języka polskiego
- Automatyczne generowanie zapytań SQL
- Obsługa zapytań JOIN, COUNT, WHERE
- Przykładowe zapytania w interfejsie
- Walidacja i obsługa błędów
- Responsywny interfejs webowy

### Security
- Tylko operacje SELECT
- Brak możliwości modyfikacji danych
- Bezpieczne przechowywanie kluczy API
- Walidacja generowanych zapytań

---

## Legenda

- `Added` - nowe funkcje
- `Changed` - zmiany w istniejących funkcjach
- `Deprecated` - funkcje które będą usunięte
- `Removed` - usunięte funkcje
- `Fixed` - naprawione błędy
- `Security` - poprawki bezpieczeństwa