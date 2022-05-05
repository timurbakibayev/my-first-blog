from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup, PageElement
import requests


@dataclass
class Flat:
    rooms: int
    price: float


def get_flats(url_: str) -> List:
    result = requests.get(url_)
    html_parse = BeautifulSoup(result.content.decode("utf8"), 'html.parser')
    return [el.get("alt") for el in html_parse.find_all("img") if el.get("alt") != "" and el.get("alt") is not None]


# url = "https://krisha.kz/prodazha/kvartiry/almaty-bostandykskij-almagul/"
url = "https://krisha.kz/prodazha/kvartiry/vostochno-kazahstanskaja-oblast/"

flats_p = get_flats(url)
flats = list()
for flat in flats_p:
    try:
        rooms = flat.split(",")[0]
        area = flat.split(",")[1]
        etaj = flat.split(",")[2]
        info = flat.split(",")[3]
        if "за" not in info:
            info += "," + flat.split(",")[4]
        if "~" in info:
            price1 = info.find("~") + 2
        else:
            price1 = info.find("за") + 3
        price2 = info.find(" ", price1)
        price = float(info[price1:price2])
        if "млн" in info:
            price *= 1_000_000
        if "млрд" in info:
            price *= 1_000_000_000
        flat = Flat(
            rooms=int(rooms.split("-")[0]),
            price=price,
        )
        flats.append(flat)
    except Exception:
        pass

prices = dict()
for flat in flats:
    if flat.rooms not in prices:
        prices[flat.rooms] = list()
    prices[flat.rooms].append(flat.price)

for rooms in prices.keys():
    print("Rooms", rooms, "Price", int(sum(prices[rooms])/len(prices[rooms])))

