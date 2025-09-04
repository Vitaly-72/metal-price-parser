# parsers/parad_parser.py
from .base_parser import BaseParser
from bs4 import BeautifulSoup
import re
from typing import List, Dict

class ParadParser(BaseParser):
    def parse_products(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'lxml')
        products = []
        
        # Поиск товаров
        product_items = soup.find_all('div', class_='product-thumb')
        
        for item in product_items:
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
                    
                    normalized = self.normalize_product_name(name)
                    
                    products.append({
                        'original_name': name,
                        'normalized_name': normalized['name'],
                        'diameter': normalized['diameter'],
                        'length': normalized['length'],
                        'price': price,
                        'source': 'Парад'
                    })
            except Exception as e:
                print(f"Error parsing Parad product: {e}")
                continue
        
        return products
    
    def normalize_product_name(self, name: str) -> Dict:
    diameter = None
    length = None
    
    # Ищем диаметр (разные варианты написания)
    diam_match = re.search(r'(\d+)\s*мм', name)
    if diam_match:
        diameter = diam_match.group(1)
    
    # Ищем длину (поддерживаем дробные числа)
    length_match = re.search(r'(\d+[\.,]?\d*)\s*м', name)
    if length_match:
        length_str = length_match.group(1).replace(',', '.')
        try:
            length = float(length_str)
        except ValueError:
            length = None
    
    normalized_name = f"Арматура {diameter or '?'} {length or '?'}м"
    
    return {
        'name': normalized_name,
        'diameter': diameter,
        'length': length
    }

# Явно экспортируем класс
__all__ = ['ParadParser']
