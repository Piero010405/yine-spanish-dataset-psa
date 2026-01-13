"""
Extractor module for scraping parallel YINE-Spanish examples.
"""
from scraper_diccionary.normalizer import clean_text
from config.constants import (
    IDIOMA_BASE,
    IDIOMA_OBJETIVO,
    EXAMPLE_SELECTOR
)

def extract_parallel_examples(item, page, logger):
    """
    Extract parallel YINE-Spanish examples from a dictionary item.
    """
    results = []

    example_block = item.select_one(EXAMPLE_SELECTOR)
    if not example_block:
        return results

    # Obtener texto respetando saltos
    raw_text = example_block.get_text(separator="\n")
    lines = [clean_text(l) for l in raw_text.split("\n") if clean_text(l)]

    # Esperamos al menos dos líneas: YINE / ESPAÑOL
    if len(lines) < 2:
        return results

    yine = lines[0]
    spa = lines[1]

    # Filtro de seguridad adicional
    if len(yine) < 2 or len(spa) < 2:
        return results

    results.append({
        "source": "diccionario_virtual_yine",
        IDIOMA_BASE: yine,
        IDIOMA_OBJETIVO: spa,
        "page": page
    })

    return results
