# config.py

# Тримет - арматура (несколько страниц)
TRIMET_ARMATURA_URLS = [
    "https://trimet.ru/catalog/chernyy_metalloprokat/armatura_1/"
]

# Парад - арматура (несколько страниц)  
PARAD_ARMATURA_URLS = [
    "https://72parad.ru/metalloprokat/armatura/"
]

# Другие категории (пример)
TRIMET_TRUBA_URLS = [
    "https://trimet.ru/catalog/chernyy_metalloprokat/truby_profilnye/?PAGEN_1=1",
    "https://trimet.ru/catalog/chernyy_metalloprokat/truby_profilnye/?PAGEN_1=2"
]

PARAD_TRUBA_URLS = [
    "https://72parad.ru/metalloprokat/truba-profilnaya/"
]
# Тестовые данные для Тримет (на основе вашего HTML)
TRIMET_TEST_DATA = [
    {"name": "Арматура 6 (3 метра)", "price": 50, "site": "Тримет"},
    {"name": "Арматура 6 (6 метров)", "price": 90, "site": "Тримет"},
    {"name": "Арматура 8 (3 метра)", "price": 80, "site": "Тримет"},
    {"name": "Арматура 8 (6 метров)", "price": 160, "site": "Тримет"},
    {"name": "Арматура 10 (5,85 метров)", "price": 230, "site": "Тримет"},
    {"name": "Арматура 12 (5,85 метров)", "price": 310, "site": "Тримет"}
]
