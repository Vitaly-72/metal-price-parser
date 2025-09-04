import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # URLs для парсинга
    TRIMET_URLS = {
        'armatura': os.getenv('TRIMET_ARMATURA_URL', ''),
        'truba_profilnaya': os.getenv('TRIMET_TRUBA_URL', '')
    }
    
    PARAD_URLS = {
        'armatura': os.getenv('PARAD_ARMATURA_URL', ''),
        'truba_profilnaya': os.getenv('PARAD_TRUBA_URL', '')
    }
    
    # Настройки парсера
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
