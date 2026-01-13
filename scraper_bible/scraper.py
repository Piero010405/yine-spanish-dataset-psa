"""
Scraper module for downloading and parsing Bible verses.
"""
import os
from bs4 import BeautifulSoup, NavigableString, Tag
import ftfy
from config.constants import (
    IDIOMA_BASE,
    RAW_DIR,
    BASE_URL_IDIOMA_BASE,
    BASE_URL_IDIOMA_OBJETIVO,
)

from config.settings import TIMEOUT
from utils.io import safe_request, ensure_dir


def save_raw_html(html, lang, book, chapter):
    """
    Guarda el HTML crudo en data/raw/<lang>/<BOOK><chapter>.htm
    """
    ensure_dir(f"{RAW_DIR}/{lang}/")
    filename = f"{book}{chapter:02d}.htm"
    path = os.path.join(RAW_DIR, lang, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

def build_url(language: str, book: str, chapter: int) -> str:
    """
    Genera la URL dinámica según el idioma, libro y capítulo.
    Usa 3 dígitos solo si el libro tiene más de 99 capítulos (como Salmos).
    """
    from lib.books_dict import BOOKS

    info = BOOKS[book]
    chapters = info["chapters"]

    # Determinar el número máximo de capítulos
    max_ch = max(chapters) if isinstance(chapters, list) else chapters

    # Formatear con 2 o 3 dígitos según corresponda
    pad = 3 if max_ch >= 100 else 2
    chapter_str = f"{chapter:0{pad}d}"

    base = BASE_URL_IDIOMA_BASE if language == IDIOMA_BASE else BASE_URL_IDIOMA_OBJETIVO
    return f"{base}/{book}{chapter_str}.htm"

def get_verses(url, lang, book, chapter, timeout=TIMEOUT):
    """
    Descarga y parsea los versículos de un capítulo.
    También guarda el HTML crudo en data/raw/ por idioma.
    """
    response = safe_request(url, timeout)
    if response is None:
        return {}  # si falla la descarga

    html = response.content.decode("utf-8", errors="ignore")

    # Guardar copia del HTML crudo
    save_raw_html(html, lang, book, chapter)

    soup = BeautifulSoup(html, "html.parser")

    verses = {}
    current_verse = None
    buffer = []

    # Iteramos por todos los divs válidos (p y q)
    valid_divs = soup.find_all("div", class_=lambda c: c in ["p", "q"])

    for div in valid_divs:
        for element in div.descendants:
            if isinstance(element, Tag):
                # Si es un nuevo versículo
                if element.name == "span" and "verse" in element.get("class", []):
                    # Guardar el anterior si hay
                    if current_verse and buffer:
                        text_clean = ftfy.fix_text(" ".join(buffer)).strip()
                        text_clean = text_clean.lstrip("0123456789 ").strip()
                        verses[current_verse] = text_clean
                        buffer = []

                    # Nuevo versículo
                    current_verse = element.get("id", "").replace("V", "").strip()

            elif isinstance(element, NavigableString):
                # Solo acumular texto si estamos dentro de un versículo
                text = element.strip()
                if text and current_verse:
                    buffer.append(text)

    # Guardar el último versículo
    if current_verse and buffer:
        text_clean = ftfy.fix_text(" ".join(buffer)).strip()
        text_clean = text_clean.lstrip("0123456789 ").strip()
        verses[current_verse] = text_clean

    return verses
