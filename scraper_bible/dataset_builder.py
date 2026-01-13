"""
Dataset builder that merges aligned chapters into a single CSV file.
"""

import os
import pandas as pd
from lib.books_dict import BOOKS
from scraper_bible.aligner import align_chapters
from config.constants import (
    OUTPUT_DIR,
    IDIOMA_BASE,
    IDIOMA_OBJETIVO
)

def build_dataset():
    """
    Builds a merged dataset of aligned Yine and Spanish Bible verses.
    Returns:
        pd.DataFrame -- DataFrame containing the merged dataset
    """
    os.makedirs(f"{OUTPUT_DIR}/merged", exist_ok=True)
    rows = []

    for book, info in BOOKS.items():
        chapters = info["chapters"]

        # Si es int → genera un rango. Si es lista → úsala directamente.
        if isinstance(chapters, int):
            chapters = range(1, chapters + 1)

        for ch in chapters:
            aligned = align_chapters(book, ch)
            if aligned:
                rows.extend(aligned)

    if not rows:
        print("⚠️ No se generaron datos alineados (revisa si hay HTMLs válidos).")
        return None

    df = pd.DataFrame(rows)
    output_path = f"{OUTPUT_DIR}/merged/{IDIOMA_BASE}_{IDIOMA_OBJETIVO}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ Dataset generado correctamente: {output_path}")
    return df
