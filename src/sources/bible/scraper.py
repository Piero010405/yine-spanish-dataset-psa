"""
Scraper module for downloading and parsing Bible verses.
Language agnostic.
"""

from bs4 import BeautifulSoup, NavigableString, Tag
import ftfy

from config.settings import (TIMEOUT, RAW_DIR )
from src.utils.io import safe_request, ensure_dir


ALLOWED_DIV_CLASSES = {"p", "q", "q1", "q2", "pi", "qc", "qt"}


def save_raw_html(html, language, book, chapter):
    """
    Save raw HTML to data/raw/<language>/bible/
    """
    path_dir = RAW_DIR / language / "bible"
    ensure_dir(path_dir)

    filename = f"{book}{chapter:02d}.htm"
    path = path_dir / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def build_url(base_url: str, book: str, chapter: int, max_chapters: int) -> str:
    """
    Build ebible URL.
    """

    pad = 3 if max_chapters >= 100 else 2
    chapter_str = f"{chapter:0{pad}d}"

    return f"{base_url}/{book}{chapter_str}.htm"


def is_allowed_div(tag: Tag) -> bool:
    """
    Check if a div tag has one of the allowed classes.
    Arguments:
    - tag: BeautifulSoup Tag object to check.
    Returns:
    - bool: True if the tag is a div with an allowed class, False otherwise.
    """
    if tag.name != "div":
        return False

    classes = tag.get("class", [])
    return any(c in ALLOWED_DIV_CLASSES for c in classes)


def get_verses(url, language, book, chapter, timeout=TIMEOUT):
    """
    Fetch and parse verses from the given URL.
    Arguments:
        - url: URL to fetch the chapter from.
        - language: Language code (e.g., 'yine' or 'spanish').
        - book: Book name (e.g., 'genesis').
        - chapter: Chapter number (e.g., 1).
        - timeout: Request timeout in seconds (default: TIMEOUT).
    Returns:
        - dict: A dictionary mapping verse numbers to verse texts.
    """
    response = safe_request(url, timeout)

    if response is None:
        return {}

    html = response.content.decode("utf-8", errors="ignore")

    save_raw_html(html, language, book, chapter)

    soup = BeautifulSoup(html, "html.parser")

    verses = {}
    current_verse = None
    buffer = []

    valid_divs = soup.find_all(is_allowed_div)

    for div in valid_divs:
        for element in div.descendants:

            if isinstance(element, Tag):

                if element.name == "span" and "verse" in element.get("class", []):

                    if current_verse and buffer:

                        text_clean = ftfy.fix_text(" ".join(buffer)).strip()
                        text_clean = text_clean.lstrip("0123456789 ").strip()

                        verses[current_verse] = text_clean
                        buffer = []

                    current_verse = element.get("id", "").replace("V", "").strip()

            elif isinstance(element, NavigableString):

                text = " ".join(element.split())

                if text and current_verse:
                    buffer.append(text)

    if current_verse and buffer:

        text_clean = ftfy.fix_text(" ".join(buffer)).strip()
        text_clean = text_clean.lstrip("0123456789 ").strip()

        verses[current_verse] = text_clean

    return verses
