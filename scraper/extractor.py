from config.constants import EXAMPLE_SELECTOR
from scraper.normalizer import clean_text

def extract_parallel_examples(item, page, logger):
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
        "yine": yine,
        "spanish": spa,
        "page": page
    })

    return results
