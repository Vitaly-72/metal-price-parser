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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    
    def parse_trimet(self, urls: List[str]) -> List[Dict]:
        """Парсим Тримет с улучшенным поиском элементов"""
        all_products = []
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"🔄 Парсим Тримет страница {i}: {url}")
                response = self.session.get(url, timeout=30)
                
                # Сохраним HTML для отладки
                with open(f'trimet_page_{i}.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Несколько вариантов поиска товаров
                items = []
                
                # Вариант 1: основной класс
                items.extend(soup.find_all('div', class_='product-list__item-roznica'))
                
                # Вариант 2: альтернативные классы
                if not items:
                    items.extend(soup.find_all('div', class_='product-item'))
                
                # Вариант 3: поиск по структуре
                if not items:
                    items.extend(soup.find_all('div', class_=re.compile('product')))
                
                print(f"Найдено элементов для анализа: {len(items)}")
                
                products = []
                for item in items:
                    product = self.parse_trimet_product(item, url)
                    if product:
                        products.append(product)
                        print(f"✅ Найден товар: {product['name']} - {product['price']} руб.")
                
                print(f"📦 Найдено товаров на странице {i}: {len(products)}")
                all_products.extend(products)
                
            except Exception as e:
                print(f"❌ Ошибка парсинга страницы {i}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        return all_products
    
    def parse_trimet_product(self, item, url: str):
        """Улучшенный парсинг товара Тримет"""
        try:
            # Несколько вариантов поиска названия
            name = None
            name_selectors = [
                'a.data_name_product',
                '.product-list__name a',
                '.product-name a',
                'h3 a',
                '.name a'
            ]
            
            for selector in name_selectors:
                name_elem = item.select_one(selector)
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    break
            
            if not name:
                return None
            
            # Несколько вариантов поиска цены
            price = None
            price_selectors = [
                '.price-type-roznica',
                '.product-price',
                '.price',
                '.product-list__price',
                '.cost'
            ]
            
            for selector in price_selectors:
                price_elem = item.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    price_match = re.search(r'(\d+[\s\d]*)\s*руб', price_text)
                    if price_match:
                        # Убираем пробелы из числа (1 000 → 1000)
                        price_str = price_match.group(1).replace(' ', '')
                        price = int(price_str)
                        break
            
            if price is None:
                print(f"⚠️ Не найдена цена для: {name}")
                return None
            
            return {
                'name': name,
                'price': price,
                'url': url,
                'site': 'Тримет'
            }
            
        except Exception as e:
            print(f"Ошибка парсинга товара: {e}")
            return None
    
    def parse_parad(self, urls: List[str]) -> List[Dict]:
        """Парсим Парад"""
        all_products = []
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"🔄 Парсим Парад страница {i}: {url}")
                response = self.session.get(url, timeout=30)
                soup = BeautifulSoup(response.text, 'lxml')
                
                items = soup.find_all('div', class_='product-thumb')
                print(f"Найдено элементов для анализа: {len(items)}")
                
                products = []
                for item in items:
                    product = self.parse_parad_product(item, url)
                    if product:
                        products.append(product)
                        print(f"✅ Найден товар: {product['name']} - {product['price']} руб.")
                
                print(f"📦 Найдено товаров на странице {i}: {len(products)}")
                all_products.extend(products)
                
            except Exception as e:
                print(f"❌ Ошибка парсинга страницы {i}: {e}")
                continue
        
        return all_products
    
    def parse_parad_product(self, item, url: str):
        """Парсим товар Парад"""
        try:
            name_elem = item.find('h4')
            if name_elem:
                name_elem = name_elem.find('a')
            if not name_elem:
                return None
            
            name = name_elem.get_text(strip=True)
            
            # Поиск цены
            price_elem = item.find('span', class_='price-new')
            if not price_elem:
                price_elem = item.find('p', class_='price')
            
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'(\d+)', price_text.replace(' ', ''))
                price = int(price_match.group(1)) if price_match else None
                
                if price:
                    return {
                        'name': name,
                        'price': price,
                        'url': url,
                        'site': 'Парад'
                    }
            
            return None
            
        except Exception as e:
            print(f"Ошибка парсинга товара Парад: {e}")
            return None

def main():
    print("🚀 Запуск улучшенного парсера...")
    
    parser = Parser()
    
    print("🔍 Начинаем парсинг Тримет...")
    trimet_products = parser.parse_trimet(TRIMET_ARMATURA_URLS)
    
    print("🔍 Начинаем парсинг Парад...")
    parad_products = parser.parse_parad(PARAD_ARMATURA_URLS)
    
    print(f"\n📊 ИТОГИ:")
    print(f"Тримет: {len(trimet_products)} товаров")
    print(f"Парад: {len(parad_products)} товаров")
    
    # Собираем результаты
    results = {
        'trimet': {
            'products': trimet_products,
            'total_count': len(trimet_products),
            'urls': TRIMET_ARMATURA_URLS
        },
        'parad': {
            'products': parad_products,
            'total_count': len(parad_products),
            'urls': PARAD_ARMATURA_URLS
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
        for product in trimet_products:
            print(f"{product['name']} - {product['price']} руб.")
    else:
        print("\n❌ Тримет: товары не найдены")
    
    if parad_products:
        print("\n=== ТОВАРЫ ПАРАД ===")
        for product in parad_products:
            print(f"{product['name']} - {product['price']} руб.")
    else:
        print("\n❌ Парад: товары не найдены")

if __name__ == "__main__":
    main()
