"""
Pipeline to scrape dictionary examples for a given language.
"""

from tqdm import tqdm

from lib.config_loader import load_language_config
from config.settings import PROCESSED_DIR
from src.sources.dictionary.fetcher import fetch_html
from src.sources.dictionary.paginator import build_page_url
from src.sources.dictionary.parser import parse_items
from src.sources.dictionary.extractor import extract_parallel_examples
from src.utils.logger import setup_logger
from src.utils.io import save_csv


def run(language: str):
    """
    Main dictionary scraping pipeline for a configured language.
    """
    cfg = load_language_config(language)

    language_src = cfg["language_code"]
    language_tgt = cfg["target_language"]

    dictionary_cfg = cfg["sources"]["dictionary"]

    base_url = dictionary_cfg["base_url"]
    list_endpoint = dictionary_cfg["list_endpoint"]
    max_page = dictionary_cfg["max_page"]
    item_selector = dictionary_cfg["item_selector"]
    example_selector = dictionary_cfg["example_selector"]
    source_name = dictionary_cfg["source_name"]

    logger = setup_logger(f"dictionary_{language}")
    parallel_sentences = []

    for page in tqdm(range(max_page + 1), desc=f"Scraping dictionary [{language}]"):
        url = build_page_url(base_url, list_endpoint, page)
        html = fetch_html(url, logger)

        if not html:
            logger.error("Failed page %s", page)
            continue

        items = parse_items(html, item_selector)

        for item in items:
            pairs = extract_parallel_examples(
                item=item,
                page=page,
                source_name=source_name,
                language_src=language_src,
                language_tgt=language_tgt,
                example_selector=example_selector,
            )
            parallel_sentences.extend(pairs)

    out_dir = PROCESSED_DIR / language_src / "corpus"
    out_dir.mkdir(parents=True, exist_ok=True)

    output_path = out_dir / f"{language_src}_{language_tgt}_dictionary.csv"

    save_csv(
        output_path,
        parallel_sentences,
        fieldnames=["source", language_src, language_tgt, "page"],
    )

    logger.info("Total dictionary pairs: %s", len(parallel_sentences))
    logger.info("Saved to: %s", output_path)


if __name__ == "__main__":
    run("yine")
