import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the dependencies
class MockOpenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key

class MockGradio:
    pass

sys.modules['openai'] = type('MockModule', (), {'OpenAI': MockOpenAI})()
sys.modules['gradio'] = MockGradio()
sys.modules['dotenv'] = type('MockModule', (), {'load_dotenv': lambda: None})()

from app import generate_natural_language_response

def test_formatting():
    print("🧪 Test formatowania odpowiedzi")
    
    # Test JOIN data
    join_data = [
        {'id': 1, 'request_date': '2025-01-15', 'status': 'otwarty', 'description': 'Problem z baterią', 'name': 'Jan Kowalski', 'email': 'jan@example.com', 'phone': '600123456'},
        {'id': 2, 'request_date': '2025-01-10', 'status': 'zamknięty', 'description': 'Pęknięty ekran', 'name': 'Anna Nowak', 'email': 'anna@example.com', 'phone': '601234567'}
    ]
    
    print("JOIN data:")
    result = generate_natural_language_response(join_data)
    print(result)
    
    # Test product data
    product_data = [
        {'id': 1, 'name': 'Laptop XYZ', 'category': 'elektronika', 'price': 3000.0, 'promotion': 1, 'stock': 15},
        {'id': 2, 'name': 'Telefon ABC', 'category': 'elektronika', 'price': 1200.0, 'promotion': 0, 'stock': 30}
    ]
    
    print("\nProduct data:")
    result = generate_natural_language_response(product_data)
    print(result)
    
    # Test COUNT data
    count_data = [{'COUNT(*)': 2}]
    
    print("\nCOUNT data:")
    result = generate_natural_language_response(count_data)
    print(result)

if __name__ == "__main__":
    test_formatting()