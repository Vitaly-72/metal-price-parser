from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import time
import random
import requests
from fp.fp import FreeProxy

class BaseParser(ABC):
    def __init__(self, timeout=60, max_retries=5, use_proxy=False):
        # ... остальной код ...
        self.use_proxy = use_proxy
        
    def get_proxy(self):
        """Получить случайный бесплатный прокси"""
        try:
            proxy = FreeProxy(rand=True, timeout=1).get()
            return {'http': proxy, 'https': proxy}
        except:
            return None
    
    def fetch_page(self, url: str) -> str:
        for attempt in range(self.max_retries):
            try:
                proxies = None
                if self.use_proxy and attempt > 1:  # Используем прокси после 2й неудачной попытки
                    proxies = self.get_proxy()
                    print(f"Using proxy: {proxies}")
                
                response = self.session.get(
                    url, 
                    timeout=self.timeout,
                    allow_redirects=True,
                    proxies=proxies
                )
                # ... остальной код ...
class BaseParser(ABC):
    def __init__(self, timeout=60, max_retries=5):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def fetch_page(self, url: str) -> str:
        for attempt in range(self.max_retries):
            try:
                print(f"Attempt {attempt + 1}/{self.max_retries} for {url}")
                
                # Добавляем случайную задержку между попытками
                if attempt > 0:
                    delay = random.uniform(2, 10)
                    print(f"Waiting {delay:.2f} seconds before retry...")
                    time.sleep(delay)
                
                response = self.session.get(
                    url, 
                    timeout=self.timeout,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                print(f"Successfully fetched {url}, status: {response.status_code}")
                return response.text
                
            except requests.exceptions.Timeout:
                print(f"Timeout on attempt {attempt + 1}")
                if attempt == self.max_retries - 1:
                    raise
                    
            except requests.exceptions.RequestException as e:
                print(f"Request error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise
                    
            except Exception as e:
                print(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    raise
                    
        return ""
