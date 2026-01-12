from config.constants import EXAMPLE_SELECTOR
from scraper.normalizer import clean_text

def extract_parallel_examples(item, page, logger):
    results = []

    example_block = item.select_one(EXAMPLE_SELECTOR)
    if not example_block:
        return results

    p_tags = example_block.find_all("p")

    if len(p_tags) >= 2:
        yine = clean_text(p_tags[0].get_text())
        spa = clean_text(p_tags[1].get_text())

    elif len(p_tags) == 1 and "<br" in str(p_tags[0]):
        parts = [clean_text(x) for x in p_tags[0].decode_contents().split("<br")]

        if len(parts) >= 2:
            yine, spa = parts[0], parts[1]
        else:
            return results
    else:
        return results

    if yine and spa:
        results.append({
            "source": "diccionario_virtual_yine",
            "yine": yine,
            "spanish": spa,
            "page": page
        })

    return results
