"""
Paginator module for building page URLs.
"""


def build_page_url(base_url: str, list_endpoint: str, page: int) -> str:
    """
    Build the paginated dictionary URL.
    Args:
        base_url (str): The base URL of the dictionary.
        list_endpoint (str): The endpoint for the word list.
        page (int): The page number to fetch.
    Returns:
        str: The complete URL for the specified page.
    """
    return f"{base_url}{list_endpoint}?combine=&page={page}"
