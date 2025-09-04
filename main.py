import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse_trimet(self, url):
        """Парсим Тримет"""
        try:
            print(f"Парсим Тримет: {url}")
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'lxml')
            
            products = []
            items = soup.find_all('div', class_='product-list__item-roznica')
            
            for item in items:
                try:
                    name_elem = item.find('a', class_='data_name_product')
                    price_elem = item.find('p', class_='price-type-roznica')
                    
                    if name_elem and price_elem:
                        name = name_elem.get_text(strip=True)
                        price_text = price_elem.get_text(strip=True)
                        
                        # Извлекаем цену
                        price_match = re.search(r'(\d+)\s*руб', price_text)
                        price = int(price_match.group(1)) if price_match else 0
                        
                        # Извлекаем диаметр и длину
                        diameter = None
                        length = None
                        
                        diam_match = re.search(r'Арматура\s*(\d+)', name)
                        if diam_match:
                            diameter = diam_match.group(1)
                        
                        length_match = re.search(r'(\d+[\.,]?\d*)\s*метр', name)
                        if length_match:
                            length_str = length_match.group(1).replace(',', '.')
                            try:
                                length = float(length_str)
                            except:
                                length = None
                        
                        products.append({
                            'name': name,
                            'price': price,
                            'diameter': diameter,
                            'length': length
                        })
                        
                except Exception as e:
                    print(f"Ошибка парсинга товара Тримет: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"Ошибка парсинга Тримет: {e}")
            return []
    
    def parse_parad(self, url):
        """Парсим Парад"""
        try:
            print(f"Парсим Парад: {url}")
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'lxml')
            
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
                        
                        # Извлекаем цену
                        price_match = re.search(r'(\d+)', price_text.replace(' ', ''))
                        price = int(price_match.group(1)) if price_match else 0
                        
                        # Извлекаем диаметр и длину
                        diameter = None
                        length = None
                        
                        diam_match = re.search(r'(\d+)\s*мм', name)
                        if diam_match:
                            diameter = diam_match.group(1)
                        
                        length_match = re.search(r'(\d+[\.,]?\d*)\s*м', name)
                        if length_match:
                            length_str = length_match.group(1).replace(',', '.')
                            try:
                                length = float(length_str)
                            except:
                                length = None
                        
                        products.append({
                            'name': name,
                            'price': price,
                            'diameter': diameter,
                            'length': length
                        })
                        
                except Exception as e:
                    print(f"Ошибка парсинга товара Парад: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"Ошибка парсинга Парад: {e}")
            return []

def main():
    print("Запуск парсера...")
    
    parser = Parser()
    
    # URLs для парсинга (замените на реальные)
    trimet_url = "https://trimet.ru/catalog/chernyy_metalloprokat/armatura_1/"
    parad_url = "https://72parad.ru/metalloprokat/armatura/"
    
    # Парсим оба сайта
    trimet_products = parser.parse_trimet(trimet_url)
    parad_products = parser.parse_parad(parad_url)
    
    print(f"Найдено товаров Тримет: {len(trimet_products)}")
    print(f"Найдено товаров Парад: {len(parad_products)}")
    
    # Собираем результаты
    results = {
        'trimet': trimet_products,
        'parad': parad_products,
        'timestamp': datetime.now().isoformat()
    }
    
    # Сохраняем в файл
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("Результаты сохранены в results.json")
    
    # Выводим результаты
    print("\n=== ТОВАРЫ ТРИМЕТ ===")
    for product in trimet_products:
        print(f"{product['name']} - {product['price']} руб.")
    
    print("\n=== ТОВАРЫ ПАРАД ===")
    for product in parad_products:
        print(f"{product['name']} - {product['price']} руб.")

if __name__ == "__main__":
    main()
