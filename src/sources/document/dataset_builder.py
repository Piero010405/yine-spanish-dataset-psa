"""
Dataset builder for document-based corpora.
"""

from src.sources.document.exporter import (
    save_document_rows_interim,
    save_document_dataset_final,
)


def build_document_dataset(
        language_src: str,
        language_tgt: str,
        rows: list[dict],
        save_xlsx: bool = True):
    """
    Builds a document-based dataset from the given rows and saves it to disk.
    Args:
        language_src (str): The source language code (e.g., 'en').
        language_tgt (str): The target language code (e.g., 'fr').
        rows (list[dict]): A list of dictionaries representing the document rows.
        save_xlsx (bool, optional): Whether to save the dataset in XLSX format. Defaults to True.
    Returns:
        str: The path to the saved dataset file.
    """
    save_document_rows_interim(language_src, rows)
    return save_document_dataset_final(language_src, language_tgt, rows, save_xlsx=save_xlsx)
