"""
Build a multilingual corpus by concatenating full corpora
from multiple languages.
"""

import argparse
import csv

import pandas as pd

from config.settings import PROCESSED_DIR


def _load_language_full_corpus(language: str):
    """
    Load full_corpus.csv for a given language if it exists.
    """
    path = PROCESSED_DIR / language / "corpus" / "full_corpus.csv"

    if not path.exists():
        print(f"⚠️ Full corpus not found for language: {language}")
        return None

    return pd.read_csv(
        path,
        sep=";",
        encoding="utf-8-sig",
        engine="python"
    )


def build_multilingual_corpus(languages: list[str]):
    """
    Build a multilingual corpus using the final per-language corpora.
    """
    frames = []

    for language in languages:
        df = _load_language_full_corpus(language)

        if df is None:
            continue

        # Detect language columns dynamically
        metadata_cols = {
            "source",
            "source_type",
            "book",
            "chapter",
            "verse",
            "page",
            "page_wampis",
            "page_spanish",
            "origin",
            "type"
        }

        lang_cols = [c for c in df.columns if c not in metadata_cols]

        if len(lang_cols) < 2:
            print(f"⚠️ Could not infer language columns for: {language}")
            continue

        # Assumption: src first, tgt second
        lang_src = lang_cols[0]
        lang_tgt = lang_cols[1]

        tmp = pd.DataFrame({
            "source_language": lang_src,
            "target_language": lang_tgt,
            "text_src": df[lang_src],
            "text_tgt": df[lang_tgt],
            "source": df["source"] if "source" in df.columns else None,
            "source_type": df["source_type"] if "source_type" in df.columns else None,
        })

        frames.append(tmp)

    if not frames:
        print("⚠️ No multilingual corpus could be built.")
        return None

    df_multi = pd.concat(frames, ignore_index=True)

    # limpieza mínima
    df_multi = df_multi.dropna(subset=["text_src", "text_tgt"])
    df_multi = df_multi[
        (df_multi["text_src"].astype(str).str.strip() != "") &
        (df_multi["text_tgt"].astype(str).str.strip() != "")
    ]

    # deduplicación
    df_multi = df_multi.drop_duplicates(
        subset=["source_language", "target_language", "text_src", "text_tgt"]
    ).reset_index(drop=True)

    out_dir = PROCESSED_DIR / "multilingual" / "corpus"
    out_dir.mkdir(parents=True, exist_ok=True)

    output_path = out_dir / "full_corpus.csv"

    df_multi.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        quoting=csv.QUOTE_ALL
    )

    print("====================================")
    print("Multilingual corpus generated")
    print(f"Rows: {len(df_multi)}")
    print(f"File: {output_path}")
    print("====================================")

    return df_multi


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--languages",
        nargs="+",
        required=True,
        help="List of language codes, e.g. yine wampis"
    )
    args = parser.parse_args()

    build_multilingual_corpus(args.languages)
