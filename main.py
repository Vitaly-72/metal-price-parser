import json
from datetime import datetime
from parsers import TrimetParser, ParadParser
from utils import ProductMatcher
from config import Config
from test_data import TRIMET_TEST_HTML, PARAD_TEST_HTML

def main():
    print("Starting metal products parser...")
    
    trimet_parser = TrimetParser(timeout=45, max_retries=3)
    parad_parser = ParadParser(timeout=45, max_retries=3)
    
    try:
        # Парсинг Тримет
        print("Parsing Trimet...")
        try:
            trimet_html = trimet_parser.fetch_page(Config.TRIMET_URLS['armatura'])
            trimet_products = trimet_parser.parse_products(trimet_html)
            print(f"Successfully parsed {len(trimet_products)} products from Trimet")
        except Exception as e:
            print(f"Failed to parse Trimet: {e}")
            print("Using test data for Trimet")
            trimet_products = trimet_parser.parse_products(TRIMET_TEST_HTML)
            print(f"Using {len(trimet_products)} test products from Trimet")
        
        # Парсинг Парад
        print("Parsing Parad...")
        try:
            parad_html = parad_parser.fetch_page(Config.PARAD_URLS['armatura'])
            parad_products = parad_parser.parse_products(parad_html)
            print(f"Successfully parsed {len(parad_products)} products from Parad")
        except Exception as e:
            print(f"Failed to parse Parad: {e}")
            print("Using test data for Parad")
            parad_products = parad_parser.parse_products(PARAD_TEST_HTML)
            print(f"Using {len(parad_products)} test products from Parad")
        
        # Сопоставление продуктов
        print("Matching products...")
        matched_products = ProductMatcher.match_products(trimet_products, parad_products)
        
        # Сохранение результатов
        output_data = {
            'matched_products': matched_products,
            'trimet_products': trimet_products,
            'parad_products': parad_products,
            'timestamp': datetime.now().isoformat(),
            'source': 'live' if 'test' not in str(trimet_products[0]) else 'test_data'
        }
        
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully matched {len(matched_products)} products")
        print("Results saved to results.json")
        
        # Вывод результатов в консоль
        print("\n=== MATCHED PRODUCTS ===")
        for product in matched_products:
            print(f"{product['name']}: Тримет: {product['prices']['Тримет']}; Парад: {product['prices']['Парад']}")
        
        print(f"\nTotal Trimet products: {len(trimet_products)}")
        print(f"Total Parad products: {len(parad_products)}")
        print(f"Matched products: {len(matched_products)}")
        
    except Exception as e:
        print(f"Critical error in main: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
