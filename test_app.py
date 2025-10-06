import sqlite3
import os
import sys
sys.path.append('.')
from app import create_sample_db, run_sql_query, generate_natural_language_response

def test_database_creation():
    """Test tworzenia bazy danych"""
    print("🧪 Test 1: Tworzenie bazy danych")
    create_sample_db('test.db')
    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    # Sprawdź tabele
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]
    print(f"Tabele: {tables}")
    
    # Sprawdź dane w tabelach
    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"Tabela {table}: {count} rekordów")
    
    conn.close()
    print("✅ Test 1 zakończony\n")

def test_simple_queries():
    """Test prostych zapytań"""
    print("🧪 Test 2: Proste zapytania")
    
    queries = [
        "SELECT COUNT(*) FROM products",
        "SELECT COUNT(*) FROM customers", 
        "SELECT COUNT(*) FROM service_requests",
        "SELECT * FROM service_requests WHERE status = 'w trakcie'"
    ]
    
    for query in queries:
        print(f"SQL: {query}")
        result = run_sql_query(query, 'test.db')
        print(f"Wynik: {result}")
        print()
    
    print("✅ Test 2 zakończony\n")

def test_join_query():
    """Test zapytania JOIN"""
    print("🧪 Test 3: Zapytanie JOIN")
    
    query = "SELECT sr.id, sr.request_date, sr.status, sr.description, c.name, c.email, c.phone FROM service_requests sr JOIN customers c ON sr.customer_id = c.id"
    print(f"SQL: {query}")
    
    result = run_sql_query(query, 'test.db')
    print(f"Surowy wynik: {result}")
    print(f"Liczba wyników: {len(result)}")
    
    if result:
        print("Pierwszy rekord:")
        for key, value in result[0].items():
            print(f"  {key}: {value}")
    
    print("✅ Test 3 zakończony\n")

def test_response_formatting():
    """Test formatowania odpowiedzi"""
    print("🧪 Test 4: Formatowanie odpowiedzi")
    
    # Test danych JOIN
    join_data = [
        {'id': 1, 'request_date': '2025-01-15', 'status': 'otwarty', 'description': 'Problem z baterią', 'name': 'Jan Kowalski', 'email': 'jan@example.com', 'phone': '600123456'},
        {'id': 2, 'request_date': '2025-01-10', 'status': 'zamknięty', 'description': 'Pęknięty ekran', 'name': 'Anna Nowak', 'email': 'anna@example.com', 'phone': '601234567'}
    ]
    
    print("Dane wejściowe:")
    for item in join_data:
        print(f"  {item}")
    
    formatted = generate_natural_language_response(join_data)
    print(f"\nSformatowana odpowiedź:\n{formatted}")
    
    # Test danych produktów
    product_data = [
        {'id': 1, 'name': 'Laptop XYZ', 'category': 'elektronika', 'price': 3000.0, 'promotion': 1, 'stock': 15}
    ]
    
    print("Dane produktów:")
    for item in product_data:
        print(f"  {item}")
    
    formatted_products = generate_natural_language_response(product_data)
    print(f"\nSformatowane produkty:\n{formatted_products}")
    
    print("✅ Test 4 zakończony\n")

def test_count_query():
    """Test zapytań COUNT"""
    print("🧪 Test 5: Zapytania COUNT")
    
    count_queries = [
        "SELECT COUNT(*) FROM service_requests WHERE status = 'w trakcie'",
        "SELECT COUNT(*) FROM products WHERE promotion = 1"
    ]
    
    for query in count_queries:
        print(f"SQL: {query}")
        result = run_sql_query(query, 'test.db')
        print(f"Surowy wynik: {result}")
        
        formatted = generate_natural_language_response(result)
        print(f"Sformatowany: {formatted}")
        print()
    
    print("✅ Test 5 zakończony\n")

def cleanup():
    """Usuń pliki testowe"""
    if os.path.exists('test.db'):
        os.remove('test.db')
    print("🧹 Pliki testowe usunięte")

if __name__ == "__main__":
    print("🚀 Uruchamianie testów funkcjonalności\n")
    
    try:
        test_database_creation()
        test_simple_queries()
        test_join_query()
        test_response_formatting()
        test_count_query()
        
        print("🎉 Wszystkie testy zakończone!")
        
    except Exception as e:
        print(f"❌ Błąd w testach: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup()