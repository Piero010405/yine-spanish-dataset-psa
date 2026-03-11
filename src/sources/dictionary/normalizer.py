"""
Normalizer module for cleaning text data.
"""

import re


def repair_encoding(text: str) -> str:
    """
    Repair multi-layer UTF-8/Latin1 mojibake safely.
    Applies iterative fixes until text stabilizes.
    Args:
        text (str): The input text to repair.
    Returns:
        str: The repaired text.
    """
    current = text

    for _ in range(3):
        try:
            fixed = current.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            break

        if fixed == current:
            break

        current = fixed

    return current


def clean_text(text: str) -> str:
    """
    Clean and normalize text by:
        - repairing mojibake
        - removing bracketed and parenthetical content
        - normalizing whitespace
    """
    if not text:
        return ""

    text = repair_encoding(text)
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()
