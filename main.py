import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict
from config import TRIMET_ARMATURA_URLS, PARAD_ARMATURA_URLS, TRIMET_TEST_DATA

class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://google.com/',
        }
    
    def parse_trimet(self, urls: List[str]) -> List[Dict]:
        """Парсим Тримет или используем тестовые данные при ошибке"""
        print("🔄 Попытка парсинга Тримет...")
        
        try:
            # Пробуем спарсить реальные данные
            url = urls[0]
            print(f"Пытаемся подключиться к: {url}")
            
            # Увеличиваем таймаут и добавляем retry
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                items = soup.find_all('div', class_='product-list__item-roznica')
                
                products = []
                for item in items:
                    product = self.parse_trimet_product(item, url)
                    if product:
                        products.append(product)
                
                print(f"✅ Успешно спарсено товаров Тримет: {len(products)}")
                return products
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                raise Exception(f"HTTP {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Ошибка парсинга Тримет: {e}")
            print("🔄 Используем тестовые данные для Тримет")
            return TRIMET_TEST_DATA
    
    def parse_trimet_product(self, item, url: str):
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
                    'url': url,
                    'site': 'Тримет'
                }
        except Exception as e:
            print(f"Ошибка парсинга товара Тримет: {e}")
        return None
    
    def parse_parad(self, urls: List[str]) -> List[Dict]:
        """Парсим Парад"""
        all_products = []
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"🔄 Парсим Парад страница {i}: {url}")
                response = self.session.get(url, timeout=15)
                
                if response.status_code != 200:
                    print(f"❌ Ошибка HTTP: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'lxml')
                items = soup.find_all('div', class_='product-thumb')
                print(f"Найдено товарных элементов: {len(items)}")
                
                products = []
                for item in items:
                    product = self.parse_parad_product(item, url)
                    if product:
                        products.append(product)
                        print(f"✅ Найден товар: {product['name']} - {product['price']} руб.")
                
                print(f"📦 Найдено товаров на странице {i}: {len(products)}")
                all_products.extend(products)
                
            except Exception as e:
                print(f"❌ Ошибка парсинга страницы Парад {i}: {e}")
                continue
        
        return all_products
    
    def parse_parad_product(self, item, url: str):
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
                    'url': url,
                    'site': 'Парад'
                }
        except Exception as e:
            print(f"Ошибка парсинга товара Парад: {e}")
        return None

def main():
    print("🚀 Запуск парсера...")
    
    parser = Parser()
    
    print("=" * 50)
    print("🔍 ПАРСИНГ ТРИМЕТ")
    print("=" * 50)
    trimet_products = parser.parse_trimet(TRIMET_ARMATURA_URLS)
    
    print("=" * 50)
    print("🔍 ПАРСИНГ ПАРАД")
    print("=" * 50)
    parad_products = parser.parse_parad(PARAD_ARMATURA_URLS)
    
    print("=" * 50)
    print("📊 ИТОГИ:")
    print("=" * 50)
    print(f"Тримет: {len(trimet_products)} товаров")
    print(f"Парад: {len(parad_products)} товаров")
    
    # Собираем результаты
    results = {
        'trimet': {
            'products': trimet_products,
            'total_count': len(trimet_products),
            'note': 'Использованы тестовые данные из-за блокировки сайта' if trimet_products == TRIMET_TEST_DATA else 'Реальные данные'
        },
        'parad': {
            'products': parad_products,
            'total_count': len(parad_products)
        },
        'timestamp': datetime.now().isoformat()
    }
    
    # Сохраняем в файл
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("💾 Результаты сохранены в results.json")
    
    # Выводим результаты
    if trimet_products:
        print("\n=== ТОВАРЫ ТРИМЕТ ===")
        for i, product in enumerate(trimet_products, 1):
            print(f"{i}. {product['name']} - {product['price']} руб.")
    
    if parad_products:
        print("\n=== ТОВАРЫ ПАРАД ===")
        for i, product in enumerate(parad_products, 1):
            print(f"{i}. {product['name']} - {product['price']} руб.")

if __name__ == "__main__":
    main()
