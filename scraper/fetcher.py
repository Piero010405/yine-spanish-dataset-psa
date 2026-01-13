"""
Fetcher module for fetching HTML content.
"""
import time
import requests
from config.settings import REQUEST_HEADERS, TIMEOUT, SLEEP_SECONDS, RETRIES

def fetch_html(url, logger):
    """
    Fetch HTML content from a given URL with retries.

    Args:
        url (str): The URL to fetch.
        logger (Logger): Logger for logging messages.
    Returns:
        str: HTML content if successful, None otherwise.
    """
    for attempt in range(RETRIES):
        try:
            r = requests.get(url, headers=REQUEST_HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            time.sleep(SLEEP_SECONDS)
            return r.text
        except Exception as e:
            logger.warning(f"Retry {attempt+1}/{RETRIES} failed: {e}")
    return None
