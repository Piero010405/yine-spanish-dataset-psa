"""
Configuration settings for the scraper.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = DATA_DIR / "logs"
DOCS_DIR = BASE_DIR / "docs"
FIGURES_DIR = DOCS_DIR / "figures"

TIMEOUT = 20
SLEEP_SECONDS = 0.7
RETRIES = 3

REQUEST_HEADERS = {
    "User-Agent": "ParallelCorpusBuilder/1.0 (academic use)"
}

# Plantilla global reutilizable para JSON intermedio de Biblia
FILENAME_TEMPLATE = "{lang}_{book}_{chapter:02d}.json"
