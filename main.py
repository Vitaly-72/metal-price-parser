import json
from datetime import datetime
from parsers import TrimetParser, ParadParser
from utils import ProductMatcher
from config import Config

def main():
    print("Starting metal products parser...")
    
    # Инициализация парсеров
    trimet_parser = TrimetParser()
    parad_parser = ParadParser()
    
    try:
        # Парсинг Тримет
        print("Parsing Trimet...")
        trimet_html = trimet_parser.fetch_page(Config.TRIMET_URLS['armatura'])
        trimet_products = trimet_parser.parse_products(trimet_html)
        
        # Парсинг Парад
        print("Parsing Parad...")
        parad_html = parad_parser.fetch_page(Config.PARAD_URLS['armatura'])
        parad_products = parad_parser.parse_products(parad_html)
        
        # Сопоставление продуктов
        print("Matching products...")
        matched_products = ProductMatcher.match_products(trimet_products, parad_products)
        
        # Сохранение результатов
        output_data = {
            'matched_products': matched_products,
            'trimet_products': trimet_products,
            'parad_products': parad_products,
            'timestamp': datetime.now().isoformat()
        }
        
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully matched {len(matched_products)} products")
        print("Results saved to results.json")
        
        # Вывод результатов в консоль
        for product in matched_products:
            print(f"{product['name']}: Тримет: {product['prices']['Тримет']}; Парад: {product['prices']['Парад']}")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
