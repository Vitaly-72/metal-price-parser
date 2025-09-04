import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict
from config import TRIMET_ARMATURA_URLS, PARAD_ARMATURA_URLS, TRIMET_TRUBA_URLS, PARAD_TRUBA_URLS

class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse_category(self, urls: List[str], site: str, category: str) -> List[Dict]:
        """Парсим категорию с нескольких страниц"""
        all_products = []
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"Парсим {site} {category} страница {i}: {url}")
                response = self.session.get(url, timeout=30)
                soup = BeautifulSoup(response.text, 'lxml')
                
                products = []
                
                if site == 'Тримет':
                    items = soup.find_all('div', class_='product-list__item-roznica')
                    for item in items:
                        product = self.parse_trimet_product(item, url, i, category)
                        if product:
                            products.append(product)
                
                elif site == 'Парад':
                    items = soup.find_all('div', class_='product-thumb')
                    for item in items:
                        product = self.parse_parad_product(item, url, i, category)
                        if product:
                            products.append(product)
                
                print(f"Найдено товаров на странице {i}: {len(products)}")
                all_products.extend(products)
                
            except Exception as e:
                print(f"Ошибка парсинга страницы {i}: {e}")
                continue
        
        return all_products
    
    def parse_trimet_product(self, item, url, page, category):
        """Парсим товар Тримет"""
        try:
            name_elem = item.find('a', class_='data_name_product')
            price_elem = item.find('p', class_='price-type-roznica')
            
            if name_elem and price_elem:
                name = name_elem.get_text(strip=True)
                price_text = price_elem.get_text(strip=True)
                
                price_match = re.search(r'(\d+)\s*руб', price_text)
                price = int(price_match.group(1)) if price_match else 0
                
                return {
                    'name': name,
                    'price': price,
                    'category': category,
                    'url': url,
                    'page': page,
                    'site': 'Тримет'
                }
        except Exception as e:
            print(f"Ошибка парсинга товара Тримет: {e}")
        return None
    
    def parse_parad_product(self, item, url, page, category):
        """Парсим товар Парад"""
        try:
            name_elem = item.find('h4')
            if name_elem:
                name_elem = name_elem.find('a')
            price_elem = item.find('span', class_='price-new')
            
            if name_elem and price_elem:
                name = name_elem.get_text(strip=True)
                price_text = price_elem.get_text(strip=True)
                
                price_match = re.search(r'(\d+)', price_text.replace(' ', ''))
                price = int(price_match.group(1)) if price_match else 0
                
                return {
                    'name': name,
                    'price': price,
                    'category': category,
                    'url': url,
                    'page': page,
                    'site': 'Парад'
                }
        except Exception as e:
            print(f"Ошибка парсинга товара Парад: {e}")
        return None

def main():
    print("Запуск парсера для нескольких категорий...")
    
    parser = Parser()
    
    # Парсим разные категории
    results = {
        'armatura': {
            'trimet': parser.parse_category(TRIMET_ARMATURA_URLS, 'Тримет', 'арматура'),
            'parad': parser.parse_category(PARAD_ARMATURA_URLS, 'Парад', 'арматура')
        },
        'truba_profilnaya': {
            'trimet': parser.parse_category(TRIMET_TRUBA_URLS, 'Тримет', 'труба профильная'),
            'parad': parser.parse_category(PARAD_TRUBA_URLS, 'Парад', 'труба профильная')
        },
        'timestamp': datetime.now().isoformat()
    }
    
    # Сохраняем в файл
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("Результаты сохранены в results.json")

if __name__ == "__main__":
    main()
