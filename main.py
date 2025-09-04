import json
from datetime import datetime
from parsers import TrimetParser, ParadParser
from utils import ProductMatcher
from config import Config
from test_data import TRIMET_TEST_HTML, PARAD_TEST_HTML

def main():
    print("Starting metal products parser...")
    
    trimet_parser = TrimetParser(timeout=45, max_retries=3)
    parad_parser = ParadParser(timeout=45, max_retries=3)
    
    try:
        # Парсинг Тримет
        print("Parsing Trimet...")
        try:
            trimet_html = trimet_parser.fetch_page(Config.TRIMET_URLS['armatura'])
            trimet_products = trimet_parser.parse_products(trimet_html)
        except Exception as e:
            print(f"Failed to parse Trimet: {e}")
            print("Using test data for Trimet")
            trimet_products = trimet_parser.parse_products(TRIMET_TEST_HTML)
        
        # Парсинг Парад
        print("Parsing Parad...")
        try:
            parad_html = parad_parser.fetch_page(Config.PARAD_URLS['armatura'])
            parad_products = parad_parser.parse_products(parad_html)
        except Exception as e:
            print(f"Failed to parse Parad: {e}")
            print("Using test data for Parad")
            parad_products = parad_parser.parse_products(PARAD_TEST_HTML)
        
        # ... остальной код без изменений ...
