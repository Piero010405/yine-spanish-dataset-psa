"""
Pipeline to download and process Bible corpus.
"""

from lib.config_loader import load_language_config

from src.sources.bible.scraper import get_verses, build_url
from src.sources.bible.processor import save_verses
from src.sources.bible.dataset_builder import build_dataset

from config.settings import TIMEOUT


def run(language):
    """
    Run the Bible source pipeline for a given language.
    """

    cfg = load_language_config(language)

    target = cfg["target_language"]

    bible_cfg = cfg["sources"]["bible"]

    base_src = bible_cfg["base_url_source"]
    base_tgt = bible_cfg["base_url_target"]

    books = bible_cfg["books"]

    for book, chapters in books.items():

        for ch in range(1, chapters + 1):

            url_src = build_url(base_src, book, ch, chapters)
            url_tgt = build_url(base_tgt, book, ch, chapters)

            print(f"{book} {ch}")

            verses_src = get_verses(url_src, language, book, ch, timeout=TIMEOUT)
            verses_tgt = get_verses(url_tgt, target, book, ch, timeout=TIMEOUT)

            if verses_src:
                save_verses(verses_src, language, book, ch)

            if verses_tgt:
                save_verses(verses_tgt, target, book, ch)

    build_dataset(language, target, books)


if __name__ == "__main__":

    run("yine")
