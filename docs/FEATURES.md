# 🚀 Funkcje SQL LLM Assistant

## 🎯 Główne funkcje

### 1. 🗣️ Natural Language Processing
- **Język polski**: Pełna obsługa zapytań w języku polskim
- **Kontekst biznesowy**: Rozumienie terminów z dziedziny e-commerce
- **Elastyczność**: Różne sposoby zadawania tego samego pytania

**Przykłady:**
```
✅ "Jakie mamy promocje?"
✅ "Pokaż produkty na promocji"
✅ "Które rzeczy są przecenione?"
```

### 2. 🤖 Inteligentne generowanie SQL
- **GPT-4o-mini**: Najnowszy model OpenAI
- **Kontekst schematu**: Automatyczne uwzględnienie struktury bazy
- **Optymalizacja**: Generowanie wydajnych zapytań

**Proces:**
1. Analiza pytania użytkownika
2. Mapowanie na schemat bazy danych
3. Generowanie zapytania SQL
4. Walidacja bezpieczeństwa
5. Wykonanie i formatowanie wyników

### 3. 🎨 Zaawansowane formatowanie
- **Inteligentne rozpoznawanie**: Różne formaty dla różnych typów danych
- **Emoji i styling**: Czytelne prezentowanie wyników
- **Kontekstowe informacje**: Dodatkowe dane w zależności od zapytania

**Typy formatowania:**
- 📦 **Produkty**: Nazwa, kategoria, cena, promocja, stan magazynowy
- 👥 **Klienci**: Imię, email, telefon
- 🎫 **Zgłoszenia**: ID, status, opis, data, dane klienta
- 📊 **Statystyki**: Liczniki, sumy, średnie

### 4. 🔒 Bezpieczeństwo
- **Tylko SELECT**: Brak możliwości modyfikacji danych
- **Walidacja SQL**: Sprawdzanie generowanych zapytań
- **Izolacja**: Bezpieczne środowisko wykonania
- **Klucze API**: Bezpieczne przechowywanie w zmiennych środowiskowych

### 5. 🎛️ Interfejs użytkownika
- **Gradio Web UI**: Nowoczesny, responsywny interfejs
- **Przykładowe zapytania**: 8 gotowych przykładów
- **Historia konwersacji**: Pełna historia zapytań i odpowiedzi
- **Real-time**: Natychmiastowe odpowiedzi

## 📊 Obsługiwane typy zapytań

### Podstawowe zapytania
```sql
-- Wszystkie produkty
SELECT * FROM products;

-- Produkty na promocji
SELECT * FROM products WHERE promotion = 1;

-- Liczba klientów
SELECT COUNT(*) FROM customers;
```

### Zapytania z filtrowaniem
```sql
-- Produkty droższe niż 1000 zł
SELECT * FROM products WHERE price > 1000;

-- Produkty z małym stanem magazynowym
SELECT * FROM products WHERE stock < 10;

-- Zgłoszenia w określonym statusie
SELECT * FROM service_requests WHERE status = 'otwarty';
```

### Zapytania JOIN
```sql
-- Zgłoszenia z danymi klientów
SELECT sr.*, c.name, c.email 
FROM service_requests sr 
JOIN customers c ON sr.customer_id = c.id;

-- Produkty ze zgłoszeniami
SELECT p.name, COUNT(sr.id) as complaints
FROM products p 
LEFT JOIN service_requests sr ON p.id = sr.product_id
GROUP BY p.id;
```

### Zapytania analityczne
```sql
-- Najdroższe produkty na promocji
SELECT * FROM products 
WHERE promotion = 1 
ORDER BY price DESC;

-- Statystyki kategorii
SELECT category, COUNT(*), AVG(price)
FROM products 
GROUP BY category;
```

## 🎯 Przypadki użycia

### 1. 🏪 E-commerce
- Sprawdzanie stanów magazynowych
- Analiza promocji i cen
- Zarządzanie kategoriami produktów

### 2. 🎧 Obsługa klienta
- Wyszukiwanie danych klientów
- Śledzenie zgłoszeń serwisowych
- Historia interakcji

### 3. 📈 Analityka biznesowa
- Raporty sprzedażowe
- Analiza trendów
- KPI i metryki

### 4. 🔍 Eksploracja danych
- Ad-hoc queries
- Szybkie sprawdzenia
- Prototypowanie raportów

## 🚀 Zaawansowane funkcje

### Inteligentne sugestie
System automatycznie sugeruje powiązane zapytania na podstawie kontekstu.

### Obsługa błędów
- Walidacja składni SQL
- Komunikaty o błędach w języku polskim
- Sugestie poprawek

### Optymalizacja wydajności
- Cache'owanie częstych zapytań
- Optymalizacja generowanych zapytań SQL
- Limit wyników dla dużych zbiorów danych

### Rozszerzalność
- Łatwe dodawanie nowych tabel
- Konfigurowalny schemat bazy
- Pluginy i rozszerzenia

## 📱 Kompatybilność

### Przeglądarki
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Systemy operacyjne
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, CentOS, etc.)

### Python
- ✅ Python 3.8+
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12