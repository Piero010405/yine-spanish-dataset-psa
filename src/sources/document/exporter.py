"""
Export utilities for document-derived corpora.
"""

import csv
import pandas as pd

from config.settings import INTERIM_DIR, PROCESSED_DIR
from src.utils.io import ensure_dir


def save_document_rows_interim(language_src: str, rows: list[dict]):
    """
    Saves the document rows to an interim CSV file for the given source language.
    Args:
        language_src (str): The source language code (e.g., 'en').
        rows (list[dict]): A list of dictionaries representing the document rows.
    Returns:
    str: The path to the saved interim CSV file, or None if no rows were provided
    """
    if not rows:
        return None

    out_dir = INTERIM_DIR / language_src / "document"
    ensure_dir(out_dir)

    output_path = out_dir / f"{language_src}_spanish_pdf.csv"

    df = pd.DataFrame(rows)
    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        quoting=csv.QUOTE_ALL,
    )

    return output_path


def save_document_dataset_final(
        language_src: str,
        language_tgt: str,
        rows: list[dict],
        save_xlsx: bool = True):
    """
    Saves the final document dataset to disk in CSV and optionally XLSX format.
    Args:
        language_src (str): The source language code (e.g., 'en').
        language_tgt (str): The target language code (e.g., 'fr').
        rows (list[dict]): A list of dictionaries representing the document rows.
        save_xlsx (bool, optional): Whether to save the dataset in XLSX format. Defaults to True.
    Returns:
        tuple: A tuple containing the paths to the saved CSV and XLSX files (if saved
    """
    out_dir = PROCESSED_DIR / language_src / "corpus"
    ensure_dir(out_dir)

    csv_path = out_dir / f"{language_src}_{language_tgt}_document.csv"
    xlsx_path = out_dir / f"{language_src}_{language_tgt}_document.xlsx"

    df = pd.DataFrame(rows)

    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        quoting=csv.QUOTE_ALL,
    )

    if save_xlsx:
        df.to_excel(xlsx_path, index=False)

    return csv_path, xlsx_path if save_xlsx else None
