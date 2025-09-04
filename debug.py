# debug.py
import requests
from bs4 import BeautifulSoup
import re

def analyze_trimet():
    url = "https://trimet.ru/catalog/chernyy_metalloprokat/armatura_1/"
    
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = session.get(url, timeout=10)
        print(f"Статус: {response.status_code}")
        
        # Сохраняем HTML для анализа
        with open('debug_trimet.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print("HTML сохранен в debug_trimet.html")
        
        # Анализируем структуру
        soup = BeautifulSoup(response.text, 'lxml')
        
        print("Поиск товарных элементов...")
        
        # Ищем конкретно товары
        product_elements = soup.find_all('div', class_='product-list__item-roznica')
        print(f"Найдено товаров: {len(product_elements)}")
        
        for i, item in enumerate(product_elements[:3]):  # Первые 3 товара
            print(f"\n--- ТОВАР {i+1} ---")
            
            # Название
            name_elem = item.find('a', class_='data_name_product')
            if name_elem:
                print(f"Название: {name_elem.get_text(strip=True)}")
            else:
                print("❌ Название не найдено")
            
            # Цена
            price_elem = item.find('p', class_='price-type-roznica')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                print(f"Цена: '{price_text}'")
                
                # Пытаемся извлечь цифры
                price_match = re.search(r'(\d+)\s*руб', price_text)
                if price_match:
                    price_str = price_match.group(1)
                    print(f"Извлеченная цена: {price_str}")
                else:
                    print("❌ Не удалось извлечь цену")
            else:
                print("❌ Цена не найдена")
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("Сайт блокирует запросы от GitHub")

if __name__ == "__main__":
    analyze_trimet()
