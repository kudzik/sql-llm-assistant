import sqlite3
import os
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

# =======================
# Konfiguracja OpenAI API
# =======================
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
    schema_info = """
SCHEMA BAZY DANYCH:
- products: id, name, category, price, promotion (1=tak, 0=nie), stock
- customers: id, name, email, phone  
- service_requests: id, customer_id, product_id, request_date, status, description

WAŻNE: 
- promotion: 1 oznacza produkt na promocji, 0 oznacza brak promocji
- Używaj tylko SELECT
- Zwróć tylko zapytanie SQL bez dodatkowych komentarzy
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Jesteś ekspertem SQL. Generuj tylko bezpieczne zapytania SELECT. Zwracaj wyłącznie kod SQL bez formatowania markdown."},
                {"role": "user", "content": f"{schema_info}\n\nPytanie: {question}\n\nSQL:"}
            ],
            max_tokens=150,
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip()
        # Usuń ewentualne markdown formatting
        if sql_query.startswith('```sql'):
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        if sql_query.startswith('```'):
            sql_query = sql_query.replace('```', '').strip()
        return sql_query
    except Exception as e:
        return f"Błąd generowania SQL: {e}"

# =======================
# Generowanie odpowiedzi naturalnym językiem
# =======================
def generate_natural_language_response(query_results):
    if isinstance(query_results, str):
        return query_results  # błąd SQL

    if not query_results:
        return "Nie znaleziono danych spełniających kryteria."

    response = ""
    for i, row in enumerate(query_results, 1):
        response += f"{i}. "
        # Formatuj czytelniej
        if 'name' in row:
            response += f"**{row['name']}**"
            if 'category' in row:
                response += f" ({row['category']})"
            if 'price' in row:
                response += f" - {row['price']} zł"
            if 'promotion' in row:
                response += f" {'🏷️ PROMOCJA' if row['promotion'] == 1 else ''}"
            if 'stock' in row:
                response += f" (stan: {row['stock']} szt.)"
        else:
            response += ", ".join([f"{k}: {v}" for k, v in row.items()])
        response += "\n"
    return response

# =======================
# Funkcja łącząca wszystkie kroki - wywoływana przez Gradio
# =======================
def chat_with_db(user_question, history):
    history = history or []
    
    # Sprawdź klucz API
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key.strip() == '':
        error_msg = "❌ Błąd: Brak klucza API OpenAI.\n\nUstaw zmienną OPENAI_API_KEY w pliku .env"
        history.append((user_question, error_msg))
        return history, history
    
    # Generuj SQL
    sql_query = generate_sql_from_question(user_question)
    
    # Sprawdź czy generowanie SQL się powiodło
    if sql_query.startswith("Błąd generowania SQL:"):
        history.append((user_question, sql_query))
        return history, history
    
    # Wykonaj zapytanie SQL
    results = run_sql_query(sql_query)
    answer = generate_natural_language_response(results)
    
    # Formatuj odpowiedź
    formatted_answer = f"🔍 **SQL:** `{sql_query}`\n\n📊 **Wynik:**\n{answer}"
    history.append((user_question, formatted_answer))
    return history, history

# =======================
# Tworzenie i uruchomienie interfejsu Gradio
# =======================
def create_gradio_interface():
    with gr.Blocks(title="SQL LLM Assistant") as demo:
        gr.Markdown("# 🤖 Asystent SQL LLM\nZadawaj pytania o dane w naturalnym języku!")
        
        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(
            label="Zadaj pytanie o dane",
            placeholder="np. Jakie mamy promocje na elektronikę?",
            lines=1
        )
        state = gr.State([])
        
        # Przykładowe pytania
        gr.Examples(
            examples=[
                "Jakie mamy promocje na elektronikę?",
                "Pokaż wszystkich klientów",
                "Ile mamy produktów w magazynie?",
                "Pokaż otwarte zgłoszenia serwisowe"
            ],
            inputs=msg
        )

        msg.submit(chat_with_db, inputs=[msg, state], outputs=[chatbot, state])
        msg.submit(lambda: "", None, msg)

    return demo

if __name__ == "__main__":
    create_sample_db()
    demo = create_gradio_interface()
    demo.launch()
