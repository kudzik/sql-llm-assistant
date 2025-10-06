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
    # Usuń starą bazę jeśli istnieje
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            promotion INTEGER,
            stock INTEGER
        )
    ''')

    c.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE service_requests (
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

    # Dodaj przykładowe dane
    # Produkty
    products = [
        ('Laptop XYZ', 'elektronika', 3000, 1, 15),
        ('Telefon ABC', 'elektronika', 1200, 0, 30),
        ('Tablet Pro', 'elektronika', 2500, 1, 8),
        ('Słuchawki Wireless', 'elektronika', 450, 0, 25),
        ('Monitor 4K', 'elektronika', 1800, 1, 12),
        ('Klawiatura Gaming', 'elektronika', 350, 0, 40),
        ('Krzesło Biurowe', 'meble', 800, 0, 5),
        ('Biurko Drewniane', 'meble', 1200, 1, 3),
        ('Lampa LED', 'meble', 150, 0, 20),
        ('Książka Python', 'książki', 80, 0, 50),
        ('Kurs SQL', 'książki', 120, 1, 15)
    ]
    c.executemany('INSERT INTO products (name, category, price, promotion, stock) VALUES (?, ?, ?, ?, ?)', products)
    
    # Klienci
    customers = [
        ('Jan Kowalski', 'jan.kowalski@example.com', '600123456'),
        ('Anna Nowak', 'anna.nowak@example.com', '601234567'),
        ('Piotr Wiśniewski', 'piotr.wisniewski@example.com', '602345678'),
        ('Maria Kowalczyk', 'maria.kowalczyk@example.com', '603456789'),
        ('Tomasz Zieliński', 'tomasz.zielinski@example.com', '604567890')
    ]
    c.executemany('INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)', customers)
    
    # Zgłoszenia serwisowe
    service_requests = [
        (1, 1, '2025-01-15', 'otwarty', 'Problem z baterią'),
        (2, 2, '2025-01-10', 'zamknięty', 'Pęknięty ekran - wymieniono'),
        (3, 3, '2025-01-12', 'w trakcie', 'Nie ładuje się tablet'),
        (1, 4, '2025-01-08', 'zamknięty', 'Słuchawki nie łączą się - naprawiono'),
        (4, 5, '2025-01-14', 'otwarty', 'Monitor migocze'),
        (5, 1, '2025-01-11', 'w trakcie', 'Laptop się przegrzewa')
    ]
    c.executemany('INSERT INTO service_requests (customer_id, product_id, request_date, status, description) VALUES (?, ?, ?, ?, ?)', service_requests)
    
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

    # Jeśli to pojedyncza wartość (np. COUNT)
    if len(query_results) == 1 and len(query_results[0]) == 1:
        key, value = list(query_results[0].items())[0]
        if 'COUNT' in key.upper():
            return f"Liczba wyników: **{value}**"
        return f"{key}: **{value}**"

    response = ""
    for i, row in enumerate(query_results, 1):
        response += f"{i}. "
        
        # Sprawdź czy to dane produktu (ma category i price)
        is_product = 'category' in row and 'price' in row
        
        if is_product:
            # Formatowanie dla produktów
            response += f"**{row.get('name', 'Nieznany')}**"
            response += f" ({row['category']})"
            response += f" - {row['price']} zł"
            if row.get('promotion') == 1:
                response += f" 🏷️ PROMOCJA"
            if 'stock' in row:
                response += f" (stan: {row['stock']} szt.)"
        else:
            # Formatowanie dla innych zapytań (w tym JOIN)
            parts = []
            for k, v in row.items():
                if k == 'id':
                    parts.append(f"ID: {v}")
                elif k == 'name':
                    parts.append(f"**{v}**")
                elif k == 'status':
                    parts.append(f"Status: {v}")
                elif k == 'description':
                    parts.append(f"Opis: {v}")
                elif k == 'request_date':
                    parts.append(f"Data: {v}")
                elif k == 'email':
                    parts.append(f"Email: {v}")
                elif k == 'phone':
                    parts.append(f"Tel: {v}")
                else:
                    parts.append(f"{k}: {v}")
            response += ", ".join(parts)
        
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
                "Pokaż zgłoszenia wraz z danymi klientów",
                "Ile mamy zgłoszeń w statusie 'w trakcie'?",
                "Pokaż produkty droższe niż 1000 zł",
                "Które produkty mają mało sztuk w magazynie?",
                "Pokaż wszystkich klientów",
                "Jakie są najdroższe produkty na promocji?",
                "Kto ma otwarte zgłoszenia?"
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
