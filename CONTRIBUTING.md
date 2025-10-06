# 🤝 Contributing to SQL LLM Assistant

Dziękujemy za zainteresowanie rozwojem projektu! Każdy wkład jest mile widziany.

## 🚀 Jak zacząć

1. **Fork** repozytorium
2. **Clone** swojego forka
3. Utwórz **branch** dla swojej funkcji (`git checkout -b feature/amazing-feature`)
4. **Commit** swoje zmiany (`git commit -m 'Add amazing feature'`)
5. **Push** do brancha (`git push origin feature/amazing-feature`)
6. Otwórz **Pull Request**

## 📋 Zasady

### Code Style
- Używaj **PEP 8** dla kodu Python
- Dodawaj **docstrings** do funkcji
- Komentarze w języku polskim lub angielskim
- Maksymalnie 88 znaków w linii

### Commits
- Używaj opisowych wiadomości commit
- Preferuj angielski w commit messages
- Format: `type: description`
  - `feat:` nowa funkcja
  - `fix:` naprawa błędu
  - `docs:` dokumentacja
  - `test:` testy

### Pull Requests
- Opisz zmiany w PR
- Dodaj testy jeśli to możliwe
- Upewnij się, że testy przechodzą
- Linkuj do powiązanych issues

## 🐛 Zgłaszanie błędów

Używaj GitHub Issues z następującymi informacjami:
- **Opis problemu**
- **Kroki do reprodukcji**
- **Oczekiwane zachowanie**
- **Aktualne zachowanie**
- **Środowisko** (OS, Python version)

## 💡 Propozycje funkcji

1. Sprawdź czy funkcja nie istnieje już w Issues
2. Opisz przypadek użycia
3. Zaproponuj implementację
4. Dodaj label `enhancement`

## 🧪 Testowanie

```bash
# Uruchom wszystkie testy
python -m pytest

# Testy jednostkowe
python test_simple.py

# Test formatowania
python test_format_only.py
```

## 📚 Rozwój lokalny

```bash
# Klonuj repozytorium
git clone https://github.com/twojaccount/sql-llm-assistant.git
cd sql-llm-assistant

# Utwórz środowisko deweloperskie
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
pip install -r requirements-dev.txt  # jeśli istnieje

# Uruchom w trybie debug
python app.py
```

## 🏷️ Versioning

Projekt używa [Semantic Versioning](https://semver.org/):
- **MAJOR**: breaking changes
- **MINOR**: nowe funkcje (backward compatible)
- **PATCH**: bug fixes

## 📞 Kontakt

- GitHub Issues: najlepszy sposób na komunikację
- Email: [twoj.email@example.com](mailto:twoj.email@example.com)

---

**Dziękujemy za wkład w rozwój projektu! 🙏**