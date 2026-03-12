"""
Merge all enabled source-level corpora for a given language
into one final corpus.
"""

import argparse
import csv
from pathlib import Path

import pandas as pd

from lib.config_loader import load_language_config
from config.settings import PROCESSED_DIR


def _load_if_exists(path: Path):
    """
    Load a CSV file if it exists.
    """
    if not path.exists():
        return None

    return pd.read_csv(
        path,
        sep=";",
        encoding="utf-8-sig",
        engine="python"
    )


def merge_language_corpus(language: str):
    """
    Merge all enabled corpora for a given language according to its YAML config.
    """
    cfg = load_language_config(language)

    language_src = cfg["language_code"]
    language_tgt = cfg["target_language"]
    sources_cfg = cfg["sources"]

    corpus_dir = PROCESSED_DIR / language_src / "corpus"
    corpus_dir.mkdir(parents=True, exist_ok=True)

    source_frames = []

    # -------------------------
    # Dictionary source
    # -------------------------
    if "dictionary" in sources_cfg and sources_cfg["dictionary"].get("enabled", False):
        dictionary_path = corpus_dir / f"{language_src}_{language_tgt}_dictionary.csv"
        df = _load_if_exists(dictionary_path)

        if df is not None:
            keep_cols = ["source", language_src, language_tgt]
            extra_cols = [c for c in ["page"] if c in df.columns]

            df = df[keep_cols + extra_cols].copy()
            df["source_type"] = "dictionary"

            source_frames.append(df)

    # -------------------------
    # Bible source
    # -------------------------
    if "bible" in sources_cfg and sources_cfg["bible"].get("enabled", False):
        bible_path = corpus_dir / f"{language_src}_{language_tgt}_bible.csv"
        df = _load_if_exists(bible_path)

        if df is not None:
            keep_cols = ["source", language_src, language_tgt]
            extra_cols = [c for c in ["book", "chapter", "verse"] if c in df.columns]

            df = df[keep_cols + extra_cols].copy()
            df["source_type"] = "bible"

            source_frames.append(df)

    # -------------------------
    # Document source
    # -------------------------
    if "document" in sources_cfg and sources_cfg["document"].get("enabled", False):
        document_path = corpus_dir / f"{language_src}_{language_tgt}_document.csv"
        df = _load_if_exists(document_path)

        if df is not None:
            keep_cols = ["source", language_src, language_tgt]
            extra_cols = [
                c for c in [
                    "page_wampis",
                    "page_spanish",
                    "page",
                    "origin",
                    "type"
                ]
                if c in df.columns
            ]

            df = df[keep_cols + extra_cols].copy()
            df["source_type"] = "document"

            source_frames.append(df)

    if not source_frames:
        print(f"⚠️ No enabled source corpora found for language: {language_src}")
        return None

    # -------------------------
    # Merge
    # -------------------------
    df_full = pd.concat(source_frames, ignore_index=True, sort=False)

    # limpieza mínima
    df_full = df_full.dropna(subset=[language_src, language_tgt])
    df_full = df_full[
        (df_full[language_src].astype(str).str.strip() != "") &
        (df_full[language_tgt].astype(str).str.strip() != "")
    ]

    # deduplicación exacta por par paralelo
    df_full = df_full.drop_duplicates(
        subset=[language_src, language_tgt]
    ).reset_index(drop=True)

    output_path = corpus_dir / "full_corpus.csv"

    df_full.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        quoting=csv.QUOTE_ALL
    )

    print("====================================")
    print(f"Final corpus generated for: {language_src}")
    print(f"Rows: {len(df_full)}")
    print(f"File: {output_path}")
    print("====================================")

    return df_full


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True, help="Language code, e.g. yine or wampis")
    args = parser.parse_args()

    merge_language_corpus(args.language)
