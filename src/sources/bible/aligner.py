"""
Align Bible chapters verse by verse.
"""

import json

from config.settings import INTERIM_DIR


def align_chapters(language_src, language_tgt, book, chapter):
    """
    Align verses from two different language versions of the same Bible chapter.
    Args:
        language_src (str): The source language code (e.g., "en" for English).
        language_tgt (str): The target language code (e.g., "es" for Spanish).
        book (str): The name of the book (e.g., "Genesis").
        chapter (int): The chapter number.
    """
    file_src = INTERIM_DIR / language_src / "bible" / f"{language_src}_{book}_{chapter:02d}.json"

    file_tgt = INTERIM_DIR / language_tgt / "bible" / f"{language_tgt}_{book}_{chapter:02d}.json"

    if not file_src.exists() or not file_tgt.exists():
        return None

    with open(file_src, encoding="utf-8") as f:
        src = json.load(f)

    with open(file_tgt, encoding="utf-8") as f:
        tgt = json.load(f)

    aligned = []

    for v in src.keys():

        if v in tgt:

            aligned.append(
                {
                    "book": book,
                    "chapter": chapter,
                    "verse": v,
                    language_src: src[v],
                    language_tgt: tgt[v],
                }
            )

    return aligned
