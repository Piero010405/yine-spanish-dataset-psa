"""
Normalizer module for cleaning text data.
"""
import re

def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace.
    Args:
        text (str): The text to clean.
    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()
