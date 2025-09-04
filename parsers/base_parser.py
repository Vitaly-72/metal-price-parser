from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import time

class BaseParser(ABC):
    def __init__(self, timeout=30, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url: str) -> str:
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)
        return ""
    
    @abstractmethod
    def parse_products(self, html: str) -> List[Dict]:
        pass
    
    @abstractmethod
    def normalize_product_name(self, name: str) -> Dict:
        pass
