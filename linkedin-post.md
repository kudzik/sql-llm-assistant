Od dawna chodziło mi po głowie pytanie:

„A gdyby tak można było po prostu rozmawiać z bazą danych – bez pisania SQL?”

W nieco ponad godzinę (łącznie z testami!) stworzyłem SQL LLM Assistant – aplikację, która łączy moc GPT-4o-mini z klasyczną bazą danych.
Dzięki niej możesz zadawać pytania w naturalnym języku, a asystent sam:

✅ generuje poprawne i bezpieczne zapytania SQL,
✅ rozumie kontekst danych,
✅ prezentuje wyniki w przejrzystej formie.

Nie musisz pamiętać nazw tabel ani pisać skomplikowanych JOIN-ów — wystarczy zwykłe pytanie, np.:
👉 „Pokaż 10 najczęściej kupowanych produktów w ostatnim miesiącu.”

Repozytorium projektu:
🔗 github.com/kudzik/sql-llm-assistant

ℹ️ Aby przetestować aplikację lokalnie, wymagane jest posiadanie aktywnego klucza API OpenAI – to właśnie dzięki niemu asystent korzysta z modeli GPT do generowania zapytań SQL.

Projekt powstał w dużej mierze dzięki Cursor AI i podejściu vibe coding – pracy w dialogu z AI, gdzie programista staje się dyrygentem idei, a nie tylko wykonawcą kodu.

To dopiero początek moich eksperymentów z AI, LLM i machine learningiem w praktyce.