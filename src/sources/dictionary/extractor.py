"""
Extractor module for scraping parallel examples from web dictionaries.
"""

from src.sources.dictionary.normalizer import clean_text


def extract_parallel_examples(
    item,
    page: int,
    source_name: str,
    language_src: str,
    language_tgt: str,
    example_selector: str,
):
    """
    Extract parallel sentence pairs from a dictionary item.
    Args:
        item: The HTML element containing the example.
        page (int): The page number for metadata.
        source_name (str): The name of the source dictionary.
        language_src (str): The source language code.
        language_tgt (str): The target language code.
        example_selector (str): The CSS selector to locate the example block.
    Returns:
        list: A list of dictionaries with parallel examples and metadata.
    """
    results = []

    example_block = item.select_one(example_selector)
    if not example_block:
        return results

    raw_text = example_block.get_text(separator="\n")
    lines = [clean_text(line) for line in raw_text.split("\n") if clean_text(line)]

    if len(lines) < 2:
        return results

    text_src = lines[0]
    text_tgt = lines[1]

    if len(text_src) < 2 or len(text_tgt) < 2:
        return results

    results.append(
        {
            "source": source_name,
            language_src: text_src,
            language_tgt: text_tgt,
            "page": page,
        }
    )

    return results
