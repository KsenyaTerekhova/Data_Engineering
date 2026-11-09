import requests
import logging
from config import API_URL

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def extract_rates() -> dict:
    """Забирает курсы валют из API."""
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Получены данные: base={data.get('base_code')}, валют={len(data.get('rates', {}))}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        raise

if __name__ == "__main__":
    data = extract_rates()
    print("Тест Extract прошел успешно!")
    print(f"Базовая валюта: {data['base_code']}")
    print(f"Курс EUR: {data['rates']['EUR']}")
