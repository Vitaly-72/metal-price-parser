import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict
from config import URLS

class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
    
    def parse_site(self, urls: List[str], site_type: str) -> List[Dict]:
        """Парсим сайт"""
        all_products = []
        
        for url in urls:
            try:
                print(f"🔗 Парсим: {url}")
                response = self.session.get(url, timeout=15)
                
                if response.status_code != 200:
                    print(f"❌ Ошибка HTTP: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'lxml')
                products = []
                
                if site_type == 'trimet':
                    products = self.parse_trimet(soup, url)
                elif site_type == 'parad':
                    products = self.parse_parad(soup, url)
                
                print(f"✅ Найдено товаров: {len(products)}")
                all_products.extend(products)
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                continue
        
        return all_products
    
    def parse_trimet(self, soup, url: str) -> List[Dict]:
        """Парсим Тримет"""
        products = []
        items = soup.find_all('div', class_='product-list__item-roznica')
        
        for item in items:
            try:
                name_elem = item.find('a', class_='data_name_product')
                price_elem = item.find('p', class_='price-type-roznica')
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    
                    price_match = re.search(r'(\d+)\s*руб', price_text)
                    price = int(price_match.group(1)) if price_match else 0
                    
                    products.append({
                        'name': name,
                        'price': price,
                        'url': url,
                        'site': 'Тримет'
                    })
                    
            except Exception as e:
                print(f"Ошибка парсинга товара Тримет: {e}")
                continue
        
        return products
    
    def parse_parad(self, soup, url: str) -> List[Dict]:
        """Парсим Парад"""
        products = []
        items = soup.find_all('div', class_='product-thumb')
        
        for item in items:
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
                    
                    products.append({
                        'name': name,
                        'price': price,
                        'url': url,
                        'site': 'Парад'
                    })
                    
            except Exception as e:
                print(f"Ошибка парсинга товара Парад: {e}")
                continue
        
        return products

def main():
    print("🚀 Запуск упрощенного парсера...")
    
    parser = Parser()
    results = {}
    
    for category, sites in URLS.items():
        print(f"\n{'='*50}")
        print(f"📦 КАТЕГОРИЯ: {category.upper()}")
        print(f"{'='*50}")
        
        category_results = {}
        
        # Парсим Тримет
        if 'trimet' in sites:
            print("🔍 Парсим Тримет...")
            trimet_products = parser.parse_site(sites['trimet'], 'trimet')
            category_results['trimet'] = {
                'products': trimet_products,
                'count': len(trimet_products)
            }
        
        # Парсим Парад
        if 'parad' in sites:
            print("🔍 Парсим Парад...")
            parad_products = parser.parse_site(sites['parad'], 'parad')
            category_results['parad'] = {
                'products': parad_products,
                'count': len(parad_products)
            }
        
        results[category] = category_results
    
    # Добавляем timestamp
    results['timestamp'] = datetime.now().isoformat()
    results['total_categories'] = len(URLS)
    
    # Сохраняем в файл
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результаты сохранены в results.json")
    
    # Выводим статистику
    print(f"\n📊 СТАТИСТИКА:")
    print(f"{'='*50}")
    for category, data in results.items():
        if category not in ['timestamp', 'total_categories']:
            trimet_count = data.get('trimet', {}).get('count', 0)
            parad_count = data.get('parad', {}).get('count', 0)
            print(f"{category}: Тримет={trimet_count}, Парад={parad_count}")

if __name__ == "__main__":
    main()
