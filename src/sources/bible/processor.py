"""
Processor module for saving processed Bible verses.
"""

import json

from config.settings import INTERIM_DIR
from src.utils.io import ensure_dir


def save_verses(verses, language, book, chapter):
    """
    Guardar versos procesados en data/interim/<language>/bible
    Arguments:
        - verses: List of verse dictionaries to save.
        - language: Language code (e.g., 'yine' or 'spanish').
        - book: Book name (e.g., 'genesis').
        - chapter: Chapter number (e.g., 1).
    """
    path_dir = INTERIM_DIR / language / "bible"

    ensure_dir(path_dir)

    filename = f"{language}_{book}_{chapter:02d}.json"
    path = path_dir / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
