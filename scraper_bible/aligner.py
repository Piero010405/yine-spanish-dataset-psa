"""
Module for aligning Yine and Spanish Bible chapters verse by verse.
"""
import json
import os
from config.constants import (
    IDIOMA_BASE,
    IDIOMA_OBJETIVO,
    OUTPUT_DIR,
    FILENAME_TEMPLATE
)

def align_chapters(book, chapter):
    """
    Aligns Yine and Spanish Bible chapters verse by verse.
    Arguments:
        book -- Book code (e.g., 'GEN' for Genesis)
        chapter -- Chapter number (int)
    Returns:
        list -- List of aligned verses as dictionaries
    """
    file_awa = os.path.join(
        OUTPUT_DIR, IDIOMA_BASE,
        FILENAME_TEMPLATE.format(lang=IDIOMA_BASE, book=book, chapter=chapter)
    )
    file_spa = os.path.join(
        OUTPUT_DIR, IDIOMA_OBJETIVO,
        FILENAME_TEMPLATE.format(lang=IDIOMA_OBJETIVO, book=book, chapter=chapter)
    )

    if not os.path.exists(file_awa) or not os.path.exists(file_spa):
        return None

    with open(file_awa, encoding="utf-8") as f:
        awa = json.load(f)
    with open(file_spa, encoding="utf-8") as f:
        spa = json.load(f)

    aligned = []
    for v in awa.keys():
        if v in spa:
            aligned.append({
                "book": book,
                "chapter": chapter,
                "verse": v,
                IDIOMA_BASE: awa[v],
                IDIOMA_OBJETIVO: spa[v]
            })
    return aligned
