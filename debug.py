# debug.py
import requests
from bs4 import BeautifulSoup

def analyze_trimet():
    url = "https://trimet.ru/catalog/chernyy_metalloprokat/armatura_1/"
    
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = session.get(url)
    
    # Сохраняем HTML для анализа
    with open('debug_trimet.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print("HTML сохранен в debug_trimet.html")
    
    # Анализируем структуру
    soup = BeautifulSoup(response.text, 'lxml')
    
    print("Поиск товарных элементов...")
    
    # Ищем все div элементы с классами содержащими product
    product_elements = soup.find_all('div', class_=lambda x: x and 'product' in x.lower())
    print(f"Найдено элементов с 'product': {len(product_elements)}")
    
    for i, elem in enumerate(product_elements[:5]):  # Первые 5 элементов
        print(f"\n--- Элемент {i+1} ---")
        print(f"Классы: {elem.get('class')}")
        print(f"HTML: {str(elem)[:200]}...")
    
    # Ищем цены
    price_elements = soup.find_all(string=re.compile(r'руб'))
    print(f"\nНайдено элементов с 'руб': {len(price_elements)}")
    
    for i, elem in enumerate(price_elements[:3]):
        print(f"Цена {i+1}: {elem}")

if __name__ == "__main__":
    analyze_trimet()
