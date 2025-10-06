Oto plan kolejnych kroków oraz przykładowy szkic kodu startowego do asystenta LLM integrującego się z lokalną bazą SQLite i generującego zapytania SQL na podstawie naturalnego języka.



## Krok 1: Przygotowanie lokalnej bazy SQLite

```python
import sqlite3

def create_sample_db(db_path='data.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            promotion INTEGER,
            stock INTEGER
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS service_requests (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            request_date TEXT,
            status TEXT,
            description TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # Przykładowe dane
    c.execute('INSERT INTO products (name, category, price, promotion, stock) VALUES (?, ?, ?, ?, ?)', 
              ('Laptop XYZ', 'elektronika', 3000, 1, 15))
    c.execute('INSERT INTO products (name, category, price, promotion, stock) VALUES (?, ?, ?, ?, ?)', 
              ('Telefon ABC', 'elektronika', 1200, 0, 30))

    c.execute('INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)', 
              ('Jan Kowalski', 'jan.kowalski@example.com', '600123456'))

    c.execute('INSERT INTO service_requests (customer_id, product_id, request_date, status, description) VALUES (?, ?, ?, ?, ?)', 
              (1, 1, '2025-10-01', 'otwarty', 'Problem z baterią'))

    conn.commit()
    conn.close()

create_sample_db()
```



## Krok 2: Funkcja wykonująca zapytania SQL na SQLite

```python
def run_sql_query(query, db_path='data.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute(query)
        rows = c.fetchall()
        columns = [desc[0] for desc in c.description]
        result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        result = f'Błąd zapytania SQL: {e}'
    conn.close()
    return result
```



## Krok 3: Funkcja integrująca się z LLM (np. OpenAI) do generowania SQL

```python
import openai

openai.api_key = 'TWÓJ_API_KEY'

def generate_sql_from_question(question):
    prompt = f"""
    Przetłumacz pytanie użytkownika na bezpieczne zapytanie SQL dla poniższej bazy danych:
    Tabele: products(id, name, category, price, promotion, stock), customers(id, name, email, phone),
    service_requests(id, customer_id, product_id, request_date, status, description).

    Pytanie: {question}
    Zapytanie SQL:
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0,
        n=1,
        stop=[";"]
    )
    sql_query = response.choices[0].text.strip()
    return sql_query
```



## Krok 4: Generowanie odpowiedzi na podstawie wyników zapytania

```python
def generate_natural_language_response(query_results):
    if isinstance(query_results, str):
        return query_results  # błąd SQL

    if not query_results:
        return "Nie znaleziono danych spełniających kryteria."

    response = "Znalezione wyniki:\n"
    for row in query_results:
        response += ", ".join([f"{k}: {v}" for k, v in row.items()]) + "\n"
    return response
```



## Krok 5: Integracja wszystkich elementów (prosty CLI)

```python
def main():
    while True:
        user_question = input("Zadaj pytanie o dane: ")
        if user_question.lower() in ["exit", "quit"]:
            break
        sql_query = generate_sql_from_question(user_question)
        print(f"Wygenerowane zapytanie SQL: {sql_query}")
        results = run_sql_query(sql_query)
        answer = generate_natural_language_response(results)
        print(f"Odpowiedź:\n{answer}\n")

if __name__ == "__main__":
    main()
```


## Rozszerzenie o Gradio

```python
import gradio as gr

def chat_with_db(user_question, history):
    sql_query = generate_sql_from_question(user_question)
    results = run_sql_query(sql_query)
    answer = generate_natural_language_response(results)
    history = history or []
    history.append((user_question, answer))
    return history, history
```

### Prosty interfejs Gradio

```python
def create_gradio_interface():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Zadaj pytanie")
        state = gr.State([])

        msg.submit(chat_with_db, inputs=[msg, state], outputs=[chatbot, state])
        msg.submit(lambda: "", None, msg)  # czyści pole input po wysłaniu

    return demo

if __name__ == "__main__":
    create_sample_db()  # tworzy bazę z danymi jeśli nie istnieje
    demo = create_gradio_interface()
    demo.launch()
```



## Co robi ten kod?

- `chat_with_db` łączy wszystkie funkcje (generowanie SQL, wykonanie, odpowiedź) i aktualizuje historię konwersacji.
- Interfejs pozwala wpisywać pytania, widzieć odpowiedzi i historię rozmowy.
- Po uruchomieniu aplikacji otwiera się przeglądarka z prostym chatem.


