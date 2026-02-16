"""
Pipeline to merge dictionary and Bible datasets
into a unified parallel corpus.
"""

import os
import csv
import pandas as pd
from config.constants import (
    PROCESSED_DIR,
    OUTPUT_DIR,
    IDIOMA_BASE,
    IDIOMA_OBJETIVO
)

def main():
    """
    Main function to merge dictionary and Bible datasets into a unified parallel corpus.
    """

    dictionary_path = f"{PROCESSED_DIR}/parallel_sentences.csv"
    bible_path = f"{OUTPUT_DIR}/{IDIOMA_BASE}_{IDIOMA_OBJETIVO}.csv"

    if not os.path.exists(dictionary_path):
        print("❌ Dictionary dataset not found.")
        return

    if not os.path.exists(bible_path):
        print("❌ Bible dataset not found.")
        return

    print("Loading datasets...")

    df_dict = pd.read_csv(dictionary_path, sep=";")
    df_bible = pd.read_csv(bible_path, sep=";")

    # Normalizar columnas mínimas
    df_dict = df_dict[[IDIOMA_BASE, IDIOMA_OBJETIVO, "source"]]
    df_bible = df_bible[[IDIOMA_BASE, IDIOMA_OBJETIVO, "source"]]

    # Concatenar
    df_full = pd.concat([df_dict, df_bible], ignore_index=True)

    # Eliminar vacíos
    df_full = df_full.dropna()
    df_full = df_full[
        (df_full[IDIOMA_BASE].str.strip() != "") &
        (df_full[IDIOMA_OBJETIVO].str.strip() != "")
    ]

    # Eliminar duplicados exactos
    df_full = df_full.drop_duplicates()

    # Crear carpeta final
    os.makedirs(f"{PROCESSED_DIR}/merged", exist_ok=True)

    output_path = f"{PROCESSED_DIR}/merged/full_corpus.csv"

    df_full.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        quoting=csv.QUOTE_ALL
    )

    print("✅ Corpus final generado:")
    print(output_path)
    print("Total samples:", len(df_full))

if __name__ == "__main__":
    main()
