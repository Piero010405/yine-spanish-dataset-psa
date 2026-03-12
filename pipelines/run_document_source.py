"""
Pipeline to process document-based corpora.
"""

import argparse
from pathlib import Path
from lib.config_loader import load_language_config
from src.sources.document.pdf_extractor import extract_parallel_pairs_from_pdf
from src.sources.document.dataset_builder import build_document_dataset


def run(language):
    """
    Run the pipeline to extract parallel text pairs from a document source (e.g. PDF)
    """
    cfg = load_language_config(language)
    language_src = cfg["language_code"]
    language_tgt = cfg["target_language"]

    document_cfg = cfg["sources"]["document"]

    if not document_cfg.get("enabled", False):
        print(f"⚠️ Document source disabled for {language}")
        return

    source_name = document_cfg["source_name"]

    pdf_cfg = document_cfg["pdf"]
    pdf_path = Path(pdf_cfg["raw_path"])
    start_page = pdf_cfg["start_page"]
    end_page = pdf_cfg["end_page"]
    column_gap_margin = pdf_cfg["column_gap_margin"]
    italic_font_markers = pdf_cfg["italic_font_markers"]

    export_cfg = document_cfg.get("export", {})
    save_xlsx = export_cfg.get("save_xlsx", True)

    rows = extract_parallel_pairs_from_pdf(
        pdf_path=pdf_path,
        source_name=source_name,
        language_src=language_src,
        language_tgt=language_tgt,
        start_page=start_page,
        end_page=end_page,
        column_gap_margin=column_gap_margin,
        italic_font_markers=italic_font_markers,
    )

    build_document_dataset(
        language_src=language_src,
        language_tgt=language_tgt,
        rows=rows,
        save_xlsx=save_xlsx,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True)
    args = parser.parse_args()
    run(args.language)
