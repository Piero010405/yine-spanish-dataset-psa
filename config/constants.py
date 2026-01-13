"""
Configuration constants for the Yine-Spanish dictionary scraper.
"""

BASE_URL = "http://diccionariovirtualyine.culturacusco.gob.pe"
LIST_ENDPOINT = "/palabra-yine-all"

MAX_PAGE = 174
ITEM_SELECTOR = "div.li-filas-data.col-md-12"
EXAMPLE_SELECTOR = "div.views-field-field-ejemplos-palabra em.field-content"

RAW_HTML_DIR = "data/raw/html"
PROCESSED_DIR = "data/processed"
LOG_DIR = "data/logs"
