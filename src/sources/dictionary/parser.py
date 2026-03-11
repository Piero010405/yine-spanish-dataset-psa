"""
Parser module for parsing HTML content.
"""

from bs4 import BeautifulSoup


def parse_items(html: str, item_selector: str):
    """
    Parse HTML content into dictionary items.
    Args:
        - html (str): The HTML content to parse.
        - item_selector (str): The CSS selector for the items in the HTML.
    Returns:
        - list: A list of parsed items matching the selector.
    """
    soup = BeautifulSoup(html, "lxml")
    return soup.select(item_selector)
