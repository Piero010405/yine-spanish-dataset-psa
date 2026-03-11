"""
Parser module for parsing HTML content.
"""
from bs4 import BeautifulSoup
from config.constants import ITEM_SELECTOR

def parse_items(html: str):
    """
    Parse HTML content into dictionary items.
    Args:
        html (str): The HTML content to parse.
    Returns:
        list: A list of parsed dictionary item elements.
    """
    soup = BeautifulSoup(html, "lxml")
    return soup.select(ITEM_SELECTOR)
