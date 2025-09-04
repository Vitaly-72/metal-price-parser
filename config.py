import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # URLs для парсинга разных категорий
    TRIMET_URLS = {
        'armatura': os.getenv('TRIMET_ARMATURA_URL', ''),
        'truba_profilnaya': os.getenv('TRIMET_TRUBA_PROFILNAYA_URL', ''),
        'ugolok': os.getenv('TRIMET_UGOLOK_URL', ''),
        'shveller': os.getenv('TRIMET_SHVELLER_URL', '')
    }
    
    PARAD_URLS = {
        'armatura': os.getenv('PARAD_ARMATURA_URL', ''),
        'truba_profilnaya': os.getenv('PARAD_TRUBA_PROFILNAYA_URL', ''),
        'ugolok': os.getenv('PARAD_UGOLOK_URL', ''),
        'shveller': os.getenv('PARAD_SHVELLER_URL', '')
    }
    
    # Настройки парсера
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
