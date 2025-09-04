import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict
from config import TRIMET_ARMATURA_URLS, PARAD_ARMATURA_URLS

class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
    
    def parse_trimet(self, urls: List[str]) -> List[Dict]:
        """Парсим Тримет"""
        all_products = []
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"🔄 Парсим Тримет страница {i}: {url}")
                response = self.session.get(url, timeout=30)
                
                if response.status_code != 200:
                    print(f"❌ Ошибка HTTP: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Ищем товары - правильный класс
                items = soup.find_all('div', class_='product-list__item-roznica')
                print(f"Найдено товарных элементов: {len(items)}")
                
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
                continue
        
        return all_products
    
    def parse_trimet_product(self, item, url: str):
        """Парсим товар Тримет"""
        try:
            # Название товара
            name_elem = item.find('a', class_='data_name_product')
            if not name_elem:
                print("❌ Не найдено название товара")
                return None
            
            name = name_elem.get_text(strip=True)
            print(f"🔍 Обрабатываем: {name}")
            
            # Цена товара
            price_elem = item.find('p', class_='price-type-roznica')
            if not price_elem:
                print("❌ Не найден элемент цены")
                return None
            
            price_text = price_elem.get_text(strip=True)
            print(f"💰 Текст цены: '{price_text}'")
            
            # Извлекаем цену
            price_match = re.search(r'(\d+[\s\d]*)\s*руб', price_text)
            if not price_match:
                print("❌ Не удалось извлечь цену из текста")
                return None
            
            price_str = price_match.group(1).replace(' ', '')
            try:
                price = int(price_str)
            except ValueError:
                print(f"❌ Не удалось преобразовать цену: {price_str}")
                return None
            
            print(f"✅ Успешно: {name} - {price} руб.")
            
            return {
                'name': name,
                'price': price,
                'url': url,
                'site': 'Тримет'
            }
            
        except Exception as e:
            print(f"❌ Ошибка парсинга товара: {e}")
            return None
    
    def parse_parad(self, urls: List[str]) -> List[Dict]:
        """Парсим Парад"""
        all_products = []
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"🔄 Парсим Парад страница {i}: {url}")
                response = self.session.get(url, timeout=30)
                
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
                print(f"❌ Ошибка парсинга страницы {i}: {e}")
                continue
        
        return all_products
    
    def parse_parad_product(self, item, url: str):
        """Парсим товар Парад"""
        try:
            # Название товара
            name_elem = item.find('h4')
            if name_elem:
                name_elem = name_elem.find('a')
            if not name_elem:
                print("❌ Не найдено название товара Парад")
                return None
            
            name = name_elem.get_text(strip=True)
            print(f"🔍 Обрабатываем Парад: {name}")
            
            # Цена товара
            price_elem = item.find('span', class_='price-new')
            if not price_elem:
                # Пробуем альтернативный поиск
                price_elem = item.find('p', class_='price')
            
            if not price_elem:
                print("❌ Не найден элемент цены Парад")
                return None
            
            price_text = price_elem.get_text(strip=True)
            print(f"💰 Текст цены Парад: '{price_text}'")
            
            # Извлекаем цену
            price_match = re.search(r'(\d+)', price_text.replace(' ', ''))
            if not price_match:
                print("❌ Не удалось извлечь цену Парад из текста")
                return None
            
            try:
                price = int(price_match.group(1))
            except ValueError:
                print(f"❌ Не удалось преобразовать цену Парад: {price_match.group(1)}")
                return None
            
            print(f"✅ Успешно Парад: {name} - {price} руб.")
            
            return {
                'name': name,
                'price': price,
                'url': url,
                'site': 'Парад'
            }
            
        except Exception as e:
            print(f"❌ Ошибка парсинга товара Парад: {e}")
            return None

def main():
    print("🚀 Запуск парсера с улучшенной отладкой...")
    
    parser = Parser()
    
    print("=" * 50)
    print("🔍 НАЧИНАЕМ ПАРСИНГ ТРИМЕТ")
    print("=" * 50)
    trimet_products = parser.parse_trimet(TRIMET_ARMATURA_URLS)
    
    print("=" * 50)
    print("🔍 НАЧИНАЕМ ПАРСИНГ ПАРАД")
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
    
    # Выводим подробные результаты
    if trimet_products:
        print("\n=== ТОВАРЫ ТРИМЕТ ===")
        for i, product in enumerate(trimet_products, 1):
            print(f"{i}. {product['name']} - {product['price']} руб.")
    else:
        print("\n❌ Тримет: товары не найдены")
        print("Проверьте:")
        print("1. Доступность сайта")
        print("2. HTML структуру")
        print("3. Блокировку парсеров")
    
    if parad_products:
        print("\n=== ТОВАРЫ ПАРАД ===")
        for i, product in enumerate(parad_products, 1):
            print(f"{i}. {product['name']} - {product['price']} руб.")

if __name__ == "__main__":
    main()
