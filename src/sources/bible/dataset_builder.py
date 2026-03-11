"""
Build final Bible dataset.
"""

import csv
import pandas as pd

from src.sources.bible.aligner import align_chapters
from config.settings import PROCESSED_DIR


def build_dataset(language_src, language_tgt, books):
    """
    Build a final Bible dataset from aligned chapters.
    Args:
        language_src (str): The source language code (e.g., "en" for English).
        language_tgt (str): The target language code (e.g., "es" for Spanish).
        books (dict): A dictionary mapping book names to the number of chapters.
    Returns:
        pd.DataFrame: The final merged dataset.
    """
    rows = []

    for book, chapters in books.items():

        for ch in range(1, chapters + 1):

            aligned = align_chapters(language_src, language_tgt, book, ch)

            if aligned:
                rows.extend(aligned)

    if not rows:
        print("⚠️ No aligned verses generated.")
        return None

    df = pd.DataFrame(rows)

    df["source"] = "bible"

    out_dir = PROCESSED_DIR / language_src / "corpus"
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / f"{language_src}_{language_tgt}_bible.csv"

    df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        quoting=csv.QUOTE_ALL,
    )

    print(f"Dataset generated: {path}")

    return df
