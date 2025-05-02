import os
import requests
import logging
import pandas as pd

from bs4 import BeautifulSoup
from typing import List


URL = "https://quotes.toscrape.com"
BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "data.xlsx")

try:
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    cards = soup.find_all("div", class_="quote")

    texts: List[str] = []
    authors: List[str] = []
    tags: List[List[str]] = []

    for card in cards:
        text: str = card.find("span", class_="text").text.strip()
        texts.append(text)

        author: str = card.find("small", class_="author").text.strip()
        authors.append(author)

        tag_list: List[str] = [card.text.strip() for card in card.find_all("a", class_="tag")]
        tags.append(", ".join(tag_list))

    data = {
        "Автор": authors,
        "Цитата": texts,
        "Тэги": tags
    }
    
    try:
        df = pd.DataFrame(data)
        df.to_excel(SAVE_DIR, index=False)
    except Exception as e:
        logging.warning(f"Ошибка сохранения данных в таблицу: {e}")
    else:
        logging.info("Данные сохранены!")

except requests.RequestException as e:
    logging.critical(f"ошибка запроса: {e}")
except Exception as e:
    logging.error(f"ошибка парсинга данных: {e}")