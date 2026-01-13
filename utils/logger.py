"""
Logger module for logging messages.
"""
import logging
import os
from config.constants import LOG_DIR

def setup_logger(name="scraper"):
    """
    Setup a logger with file and console handlers.
    Args:
        name (str): Name of the logger.
    Returns:
        Logger: Configured logger instance.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(f"{LOG_DIR}/scraping.log", encoding="utf-8")
    sh = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
