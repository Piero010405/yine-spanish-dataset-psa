"""
Normalizer module for cleaning text data.
"""
import re

def repair_encoding(text: str) -> str:
    """
    Repair multi-layer UTF-8/Latin1 mojibake safely.
    Applies iterative fixes until text stabilizes.
    """
    current = text

    for _ in range(3):  # máximo 3 capas de reparación
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
    Clean and normalize text by removing extra whitespace.
    - fixing mojibake (encoding errors)
    - removing extra whitespace
    Args:
        text (str): The text to clean.
    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""

    text = repair_encoding(text)

    # Eliminar contenido entre corchetes
    text = re.sub(r"\[[^\]]*\]", "", text)

    # Eliminar contenido entre parentesis
    text = re.sub(r"\([^)]*\)", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
