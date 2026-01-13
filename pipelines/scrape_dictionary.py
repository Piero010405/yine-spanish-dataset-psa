"""
Scrape dictionary entries and extract parallel sentences.
"""

from tqdm import tqdm
from scraper.fetcher import fetch_html
from scraper.paginator import build_page_url
from scraper.parser import parse_items
from scraper.extractor import extract_parallel_examples
from utils.logger import setup_logger
from utils.io import save_csv
from config.constants import MAX_PAGE, PROCESSED_DIR

def main():
    """
    Main function to scrape dictionary entries and save parallel sentences.
    """
    logger = setup_logger()
    parallel_sentences = []

    for page in tqdm(range(MAX_PAGE + 1), desc="Scraping pages"):
        url = build_page_url(page)
        html = fetch_html(url, logger)

        if not html:
            logger.error("Failed page %s", page)
            continue

        items = parse_items(html)

        for item in items:
            pairs = extract_parallel_examples(item, page, logger)
            parallel_sentences.extend(pairs)

    save_csv(
        f"{PROCESSED_DIR}/parallel_sentences.csv",
        parallel_sentences,
        fieldnames=["source", "yine", "spanish", "page"]
    )

    logger.info("Total parallel pairs: %s", len(parallel_sentences))

if __name__ == "__main__":
    main()
