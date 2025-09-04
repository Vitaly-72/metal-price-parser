# main.py
import json
from datetime import datetime

# Прямой импорт для отладки
try:
    from parsers.trimet_parser import TrimetParser
    from parsers.parad_parser import ParadParser
    from utils.product_matcher import ProductMatcher
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Trying alternative import...")
    # Альтернативный вариант
    import sys
    sys.path.append('.')
    from parsers.trimet_parser import TrimetParser
    from parsers.parad_parser import ParadParser
    from utils.product_matcher import ProductMatcher

from config import Config
from test_data import TRIMET_TEST_HTML, PARAD_TEST_HTML

def main():
    print("Starting metal products parser...")
    
    # Создаем экземпляры парсеров
    trimet_parser = TrimetParser(timeout=10, max_retries=1)
    parad_parser = ParadParser(timeout=10, max_retries=1)
    
    print("✅ Parsers created successfully")
    
    # Используем тестовые данные для демонстрации
    print("Using test data...")
    
    trimet_products = trimet_parser.parse_products(TRIMET_TEST_HTML)
    parad_products = parad_parser.parse_products(PARAD_TEST_HTML)
    
    print(f"Trimet products: {len(trimet_products)}")
    print(f"Parad products: {len(parad_products)}")
    
    # Сопоставление продуктов
    matched_products = ProductMatcher.match_products(trimet_products, parad_products)
    
    # Сохранение результатов
    output_data = {
        'matched_products': matched_products,
        'trimet_products_count': len(trimet_products),
        'parad_products_count': len(parad_products),
        'matched_count': len(matched_products),
        'timestamp': datetime.now().isoformat(),
        'note': 'Test data used for demonstration'
    }
    
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Successfully matched {len(matched_products)} products")
    print("✅ Results saved to results.json")
    
    # Вывод результатов
    print("\n=== MATCHED PRODUCTS ===")
    for product in matched_products:
        print(f"{product['name']}: Тримет: {product['prices']['Тримет']}; Парад: {product['prices']['Парад']}")

if __name__ == "__main__":
    main()
