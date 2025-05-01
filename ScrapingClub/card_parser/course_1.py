import requests, os, logging 
import pandas as pd

from bs4 import BeautifulSoup


# Настройка логирования
logging.basicConfig(level=logging.INFO)

URL = "https://scrapingclub.com/exercise/list_basic/?page=1"
BASE_DIR = os.path.dirname(__file__)
FILE_DIR = os.path.join(BASE_DIR, "data.xlsx")

try:
    # Получаем ответ от сайта
    response = requests.get(URL)
    response.raise_for_status()  # Вызывает исключение для HTTP ошибок

    soup = BeautifulSoup(response.text, "lxml")

    # Находим все блоки div с классом w-full rounded border
    cards = soup.find_all("div", class_="w-full rounded border")

    names = []
    prices = []
    img_urls = []

    # Проходимся по каждой карточке, извлекая данные
    for card in cards:
        name_tag = card.find("h4")
        price_tag = card.find("h5")
        img_tag = card.find("a").find("img")

        # Проверка на наличия элемента в карточке
        if name_tag and price_tag and img_tag:
            name = name_tag.text.strip()
            price = price_tag.text.strip()
            img_url = "https://scrapingclub.com" + img_tag.get("src")

            names.append(name)
            prices.append(price)
            img_urls.append(img_url)
        else:
            logging.warning("Один из элементов отсутствует в карточке.")

    data = {
        "Названия": names,
        "Цена": prices,
        "Ссылка на изображение": img_urls
    }

    # Сохраняем данные в Excel таблицу
    try:
        df = pd.DataFrame(data)
        df.to_excel(FILE_DIR, index=False)
        logging.info("Данные успешно сохранены в таблицу!")
    except Exception as e:
        logging.error(f"Ошибка сохранения данных в таблицу: {e}")

except requests.RequestException as e:
    logging.error(f"Ошибка запроса: {e}")
except Exception as e:
    logging.error(f"Ошибка парсинга данных: {e}")
