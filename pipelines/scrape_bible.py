"""
Pipeline para descargar y procesar los versículos de la Biblia.
"""

from scraper_bible.scraper import get_verses, build_url
from scraper_bible.processor import save_verses
from scraper_bible.dataset_builder import build_dataset
from lib.books_dict import BOOKS
from config.settings import TIMEOUT
from config.constants import (
    IDIOMA_BASE,
    IDIOMA_OBJETIVO
)

def main():
    """
    Función principal para ejecutar el pipeline de descarga y procesamiento de la Biblia.
    """
    for book, info in BOOKS.items():
        chapters = info["chapters"]

        # Validar si chapters es int o lista
        if isinstance(chapters, int):
            chapters = range(1, chapters + 1)

        for ch in chapters:
            for lang in [IDIOMA_BASE, IDIOMA_OBJETIVO]:
                url = build_url(lang, book, ch)
                print(f"Descargando {book} {ch} ({lang}) → {url}")

                try:
                    verses = get_verses(url, lang, book, ch, timeout=TIMEOUT)
                    if verses:
                        save_verses(verses, lang, book, ch)
                except Exception as e:
                    print(f"⚠️ Error procesando {book} {ch} ({lang}): {e}")

    print("Construyendo dataset final...")
    build_dataset()
    print("✅ Dataset generado correctamente.")

if __name__ == "__main__":
    main()
