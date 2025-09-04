# parsers/trimet_parser.py
from .base_parser import BaseParser
from bs4 import BeautifulSoup
import re
from typing import List, Dict

class TrimetParser(BaseParser):
    def parse_products(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Поиск товаров
        product_items = soup.find_all('div', class_='product-list__item-roznica')
        
        for item in product_items:
            try:
                name_elem = item.find('a', class_='data_name_product')
                price_elem = item.find('p', class_='price-type-roznica')
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    
                    # Извлекаем цену
                    price_match = re.search(r'(\d+)\s*руб', price_text)
                    price = int(price_match.group(1)) if price_match else 0
                    
                    normalized = self.normalize_product_name(name)
                    
                    products.append({
                        'original_name': name,
                        'normalized_name': normalized['name'],
                        'diameter': normalized['diameter'],
                        'length': normalized['length'],
                        'price': price,
                        'source': 'Тримет'
                    })
            except Exception as e:
                print(f"Error parsing Trimet product: {e}")
                continue
        
        return products
    
    def normalize_product_name(self, name: str) -> Dict:
        diameter = None
        length = None
        
        # Ищем диаметр
        diam_match = re.search(r'Арматура\s*(\d+)', name)
        if diam_match:
            diameter = diam_match.group(1)
        
        # Ищем длину
        length_match = re.search(r'(\d+[\.,]?\d*)\s*метр', name)
        if length_match:
            length_str = length_match.group(1).replace(',', '.')
            length = float(length_str)
        
        normalized_name = f"Арматура {diameter or '?'} {length or '?'}м"
        
        return {
            'name': normalized_name,
            'diameter': diameter,
            'length': length
        }

# Явно экспортируем класс
__all__ = ['TrimetParser']
