import os
import logging
import requests, pandas as pd
from bs4 import BeautifulSoup


URL: str = "https://scrapingclub.com/exercise/list_basic/?page=1"
BASE_DIR: str = os.path.dirname(__file__)
FILE_DIR: str =  os.path.join(BASE_DIR, "data.xlsx")

try:
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    panel = soup.find("div", class_="flex flex-row flex-wrap")
    column = panel.find("div", class_="px-4 mb-6 w-full sm:w-1/3 md:w-1/4 lg:w-4/12").find("div", class_="flex-col space-y-4 max-w-full prose")
    blocks = column.find_all("div", class_="border-b")
    
    titles: list = []
    links: list = []
    descriptions: list = []

    for block in blocks:
        title = block.find("a").text.strip()
        titles.append(title)

        description = block.find("p").text.strip()
        descriptions.append(description)

        link = "https://scrapingclub.com" + block.find("a").get("href")
        links.append(link)

    data: dict = {
        "Заголовки": titles,
        "Ссылки с заголовков": links,
        "Описания": descriptions
    }

    try:
        df = pd.DataFrame(data)
        df.to_excel(FILE_DIR, index=False)
        logging.info("Данные успешно сохранены!")
    except Exception as e:
        logging.error(f"Ошибка сохранения данных в таблицу: {e}")

except requests.RequestException as e:
    logging.critical(f"Ошибка запроса на сайт: {e}")
except Exception as e:
    logging.error(f"Ошибка парсинга: {e}")