"""
Paginator module for building page URLs.
"""
from config.constants import BASE_URL, LIST_ENDPOINT

def build_page_url(page: int) -> str:
    """
    Build the URL for a given page number.
    """
    return f"{BASE_URL}{LIST_ENDPOINT}?combine=&page={page}"
