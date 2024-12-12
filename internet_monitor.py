import requests
import logging
import time
from logging.handlers import RotatingFileHandler
from ping3 import ping


logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler('internet_monitor.log', maxBytes=50*1024*1024, backupCount=5, encoding='utf-8')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def monitor_internet():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            # Получаем пинг до Google
            ping_time = ping('www.google.com')
            logger.info(f"Интернет есть. Пинг: {ping_time:.2f} мс")
        else:
            logger.warning(f"Ошибка доступа к Google: статус {response.status_code}.")
    except requests.RequestException:
        logger.error("Интернет пропал.")

def main():
    while True:
        monitor_internet()
        time.sleep(60)

if __name__ == "__main__":
    main()
