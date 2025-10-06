def generate_natural_language_response(query_results):
    """Skopiowana funkcja formatowania z app.py"""
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