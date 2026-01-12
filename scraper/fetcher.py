import time
import requests
from config.settings import REQUEST_HEADERS, TIMEOUT, SLEEP_SECONDS, RETRIES

def fetch_html(url, logger):
    for attempt in range(RETRIES):
        try:
            r = requests.get(url, headers=REQUEST_HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            time.sleep(SLEEP_SECONDS)
            return r.text
        except Exception as e:
            logger.warning(f"Retry {attempt+1}/{RETRIES} failed: {e}")
    return None
