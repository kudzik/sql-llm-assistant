import sqlite3
import openai
import gradio as gr

# =======================
# Konfiguracja OpenAI API
# =======================
openai.api_key = 'TWÓJ_API_KEY'  # Zamień na swój klucz

# =======================
# Tworzenie przykładowej bazy SQLite
# =======================
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

    # Dodaj przykładowe dane (jeśli tabele są puste)
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
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

# =======================
# Funkcja wykonująca zapytania SQL
# =======================
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

# =======================
# Generowanie SQL z pytania użytkownika przez OpenAI
# =======================
def generate_sql_from_question(question):
    prompt = f"""
    Przetłumacz pytanie użytkownika na bezpieczne zapytanie SQL dla bazy danych z tabelami:
    products(id, name, category, price, promotion, stock), customers(id, name, email, phone),
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

# =======================
# Generowanie odpowiedzi naturalnym językiem
# =======================
def generate_natural_language_response(query_results):
    if isinstance(query_results, str):
        return query_results  # błąd SQL

    if not query_results:
        return "Nie znaleziono danych spełniających kryteria."

    response = "Znalezione wyniki:\n"
    for row in query_results:
        response += ", ".join([f"{k}: {v}" for k, v in row.items()]) + "\n"
    return response

# =======================
# Funkcja łącząca wszystkie kroki - wywoływana przez Gradio
# =======================
def chat_with_db(user_question, history):
    sql_query = generate_sql_from_question(user_question)
    results = run_sql_query(sql_query)
    answer = generate_natural_language_response(results)
    history = history or []
    history.append((user_question, answer))
    return history, history

# =======================
# Tworzenie i uruchomienie interfejsu Gradio
# =======================
def create_gradio_interface():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Zadaj pytanie")
        state = gr.State([])

        msg.submit(chat_with_db, inputs=[msg, state], outputs=[chatbot, state])
        msg.submit(lambda: "", None, msg)  # czyści pole input po wysłaniu

    return demo

if __name__ == "__main__":
    create_sample_db()
    demo = create_gradio_interface()
    demo.launch()
