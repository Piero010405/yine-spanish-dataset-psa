"""
Processor module for saving processed data.
"""
import json
import os
from config.constants import (
    OUTPUT_DIR,
    FILENAME_TEMPLATE
)
from utils.io import ensure_dir

def save_verses(verses, lang, book, chapter):
    """
    Saves the processed verses to a JSON file.
    Arguments:
        verses -- Dictionary of verses to save
        lang -- Language code (e.g., 'yine' or 'spanish')
        book -- Book code (e.g., 'GEN' for Genesis)
        chapter -- Chapter number (int)
    Returns:
        None
    """
    ensure_dir(f"{OUTPUT_DIR}/{lang}/")
    filename = FILENAME_TEMPLATE.format(lang=lang, book=book, chapter=chapter)
    path = os.path.join(OUTPUT_DIR, lang, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
