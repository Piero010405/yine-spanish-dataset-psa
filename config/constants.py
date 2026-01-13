"""
Configuration constants for the Yine-Spanish dictionary scraper.
"""

# * Language Codes
IDIOMA_BASE = "yine"
IDIOMA_OBJETIVO = "spanish"

# * Constants for Yine Diccionary Scraper
BASE_URL = "http://diccionariovirtualyine.culturacusco.gob.pe"
LIST_ENDPOINT = "/palabra-yine-all"

MAX_PAGE = 174
ITEM_SELECTOR = "div.li-filas-data.col-md-12"
EXAMPLE_SELECTOR = "div.views-field-field-ejemplos-palabra em.field-content"

# * Constants for ebible.org/ Web Scraper
BASE_URL_AWAJUN = "https://ebible.org/pibNT/"
BASE_URL_SPANISH = "https://ebible.org/spabes/"

OUTPUT_DIR = "data/processed/"
RAW_DIR = "data/raw/"

# Estructura de los archivos generados
FILENAME_TEMPLATE = "{lang}_{book}_{chapter:02d}.json"

# * Constansts for Data Storage
RAW_HTML_DIR = "data/raw/html"
PROCESSED_DIR = "data/processed"
LOG_DIR = "data/logs"
