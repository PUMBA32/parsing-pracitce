import requests
import os
import json

from bs4 import BeautifulSoup


# URL = "https://health-diet.ru/table_calorie/"

BASE_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.join(BASE_DIR, "index.html")
JSON_PATH = os.path.join(BASE_DIR, "all_categories_dict.json")
DATA_PATH = os.path.join(BASE_DIR, "data")

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0"
}

# response = requests.get(URL, headers=headers)
# src = response.text

# with open(SRC_PATH, 'w', encoding="utf-8") as file: 
#     file.write(src)

# with open(SRC_PATH, 'r', encoding="utf-8") as file: 
#     src: str = file.read()

# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

# all_categories_dict = {}

# for item in all_products_hrefs:
#     item_text: str = item.text
#     item_href: str = "https://health-diet.ru" + item['href']
    
#     all_categories_dict[item_text] = item_href

# with open(JSON_PATH, 'w', encoding='utf-8') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


with open(JSON_PATH, 'r', encoding='utf-8') as file:
    all_categories: dict = json.load(file)

count = 1
for cat_name, cat_href in all_categories.items():
    rep = [',', " ", "-", "'"]

    if count == 2: break

    for item in rep:
        if item in cat_name:
            cat_name = cat_name.replace(item, "_")
    
    response = requests.get(cat_href, headers=headers)
    src = response.text

    with open(f"{DATA_PATH}/{count}_{cat_name}.html", 'w', encoding='utf-8') as file:
        file.write(src)

    soup = BeautifulSoup(src, "lxml")

    count += 1