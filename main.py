import json
from datetime import datetime

# Прямой импорт
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
    
    # Используем тестовые данные
    print("Using test data...")
    
    # Парсим данные
    trimet_products = trimet_parser.parse_products(TRIMET_TEST_HTML)
    parad_products = parad_parser.parse_products(PARAD_TEST_HTML)
    
    print(f"\n=== TRIMET PRODUCTS ({len(trimet_products)}) ===")
    for i, product in enumerate(trimet_products, 1):
        print(f"{i}. {product['original_name']} -> {product['normalized_name']} - {product['price']} руб.")
    
    print(f"\n=== PARAD PRODUCTS ({len(parad_products)}) ===")
    for i, product in enumerate(parad_products, 1):
        print(f"{i}. {product['original_name']} -> {product['normalized_name']} - {product['price']} руб.")
    
    # Сопоставление продуктов
    print("\n=== MATCHING PRODUCTS ===")
    matched_products = ProductMatcher.match_products(trimet_products, parad_products)
    
    # Сохранение результатов
    output_data = {
        'matched_products': matched_products,
        'trimet_products': trimet_products,
        'parad_products': parad_products,
        'trimet_products_count': len(trimet_products),
        'parad_products_count': len(parad_products),
        'matched_count': len(matched_products),
        'timestamp': datetime.now().isoformat(),
        'note': 'Test data used for demonstration'
    }
    
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully matched {len(matched_products)} products")
    print("✅ Results saved to results.json")
    
    # Вывод результатов
    print("\n=== FINAL MATCHED PRODUCTS ===")
    for product in matched_products:
        print(f"{product['name']}: Тримет: {product['prices']['Тримет']}; Парад: {product['prices']['Парад']}")
    
    # Статистика
    print(f"\n=== STATISTICS ===")
    print(f"Total Trimet products: {len(trimet_products)}")
    print(f"Total Parad products: {len(parad_products)}")
    print(f"Successfully matched: {len(matched_products)}")
    print(f"Match rate: {(len(matched_products) / min(len(trimet_products), len(parad_products)) * 100):.1f}%")

if __name__ == "__main__":
    main()
