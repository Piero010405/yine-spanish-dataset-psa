from bs4 import BeautifulSoup
from config.constants import ITEM_SELECTOR

def parse_items(html: str):
    soup = BeautifulSoup(html, "lxml")
    return soup.select(ITEM_SELECTOR)
