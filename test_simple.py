import sqlite3
import os

def create_test_db():
    """Utwórz testową bazę danych"""
    if os.path.exists('test.db'):
        os.remove('test.db')
    
    conn = sqlite3.connect('test.db')
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
            description TEXT
        )
    ''')

    # Dane
    products = [
        ('Laptop XYZ', 'elektronika', 3000, 1, 15),
        ('Telefon ABC', 'elektronika', 1200, 0, 30),
        ('Tablet Pro', 'elektronika', 2500, 1, 8)
    ]
    c.executemany('INSERT INTO products (name, category, price, promotion, stock) VALUES (?, ?, ?, ?, ?)', products)
    
    customers = [
        ('Jan Kowalski', 'jan.kowalski@example.com', '600123456'),
        ('Anna Nowak', 'anna.nowak@example.com', '601234567'),
        ('Piotr Wiśniewski', 'piotr.wisniewski@example.com', '602345678')
    ]
    c.executemany('INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)', customers)
    
    service_requests = [
        (1, 1, '2025-01-15', 'otwarty', 'Problem z baterią'),
        (2, 2, '2025-01-10', 'zamknięty', 'Pęknięty ekran - wymieniono'),
        (3, 3, '2025-01-12', 'w trakcie', 'Nie ładuje się tablet')
    ]
    c.executemany('INSERT INTO service_requests (customer_id, product_id, request_date, status, description) VALUES (?, ?, ?, ?, ?)', service_requests)
    
    conn.commit()
    conn.close()

def test_join_query():
    """Test zapytania JOIN"""
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    query = "SELECT sr.id, sr.request_date, sr.status, sr.description, c.name, c.email, c.phone FROM service_requests sr JOIN customers c ON sr.customer_id = c.id"
    
    c.execute(query)
    rows = c.fetchall()
    columns = [desc[0] for desc in c.description]
    result = [dict(zip(columns, row)) for row in rows]
    
    print("🧪 Test JOIN Query")
    print(f"SQL: {query}")
    print(f"Kolumny: {columns}")
    print(f"Liczba wyników: {len(result)}")
    print("\nWyniki:")
    for i, row in enumerate(result, 1):
        print(f"{i}. {row}")
    
    conn.close()
    return result

def test_count_query():
    """Test zapytania COUNT"""
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    query = "SELECT COUNT(*) FROM service_requests WHERE status = 'w trakcie'"
    
    c.execute(query)
    rows = c.fetchall()
    columns = [desc[0] for desc in c.description]
    result = [dict(zip(columns, row)) for row in rows]
    
    print("\n🧪 Test COUNT Query")
    print(f"SQL: {query}")
    print(f"Kolumny: {columns}")
    print(f"Wynik: {result}")
    
    conn.close()
    return result

def format_response(query_results):
    """Uproszczona funkcja formatowania"""
    if not query_results:
        return "Brak wyników"
    
    # COUNT query
    if len(query_results) == 1 and len(query_results[0]) == 1:
        key, value = list(query_results[0].items())[0]
        if 'COUNT' in key.upper():
            return f"Liczba wyników: {value}"
    
    # Normalne wyniki
    response = ""
    for i, row in enumerate(query_results, 1):
        response += f"{i}. "
        parts = []
        for k, v in row.items():
            parts.append(f"{k}: {v}")
        response += ", ".join(parts) + "\n"
    
    return response

if __name__ == "__main__":
    print("🚀 Testy bez zależności zewnętrznych\n")
    
    create_test_db()
    
    # Test JOIN
    join_results = test_join_query()
    formatted_join = format_response(join_results)
    print(f"\nSformatowane JOIN:\n{formatted_join}")
    
    # Test COUNT
    count_results = test_count_query()
    formatted_count = format_response(count_results)
    print(f"\nSformatowane COUNT:\n{formatted_count}")
    
    # Cleanup
    if os.path.exists('test.db'):
        os.remove('test.db')
    
    print("✅ Testy zakończone")