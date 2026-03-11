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
        - url (str): The URL to fetch.
        - logger: Logger for logging retry attempts and errors.
    Returns:
        - str: The HTML content if successful, None otherwise.
    """
    for attempt in range(RETRIES):
        try:
            response = requests.get(url, headers=REQUEST_HEADERS, timeout=TIMEOUT)
            response.raise_for_status()

            html = response.content.decode("utf-8", errors="strict")

            time.sleep(SLEEP_SECONDS)
            return html

        except (requests.RequestException, UnicodeDecodeError) as e:
            logger.warning(f"Retry {attempt + 1}/{RETRIES} failed: {e}")

    return None
