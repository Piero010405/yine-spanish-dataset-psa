"""
PDF extractor for bilingual document-based corpora.
"""

import pdfplumber

from src.sources.document.normalizer import (
    normalize,
    clean_wampis_text,
    clean_spanish_text,
    looks_like_viable_spanish_segment,
    extract_last_wampis_candidate,
    remove_embedded_page_digits_from_wampis,
    join_spanish_fragments,
)


def is_italic(char: dict, italic_font_markers: list[str]) -> bool:
    """
    Is the character italic based on its font name containing any of the specified markers
    """
    fontname = char.get("fontname", "") or ""
    return any(marker in fontname for marker in italic_font_markers)


def dedupe_overlapped_chars(chars):
    """
    Deduplicates characters that have the same text and approximately
    the same position and font attributes,
    """
    seen = set()
    result = []

    for ch in chars:
        key = (
            ch.get("text", ""),
            round(ch.get("x0", 0), 1),
            round(ch.get("x1", 0), 1),
            round(ch.get("top", 0), 1),
            round(ch.get("bottom", 0), 1),
            ch.get("fontname", ""),
            round(ch.get("size", 0), 1),
        )
        if key not in seen:
            seen.add(key)
            result.append(ch)

    return result


def extract_parallel_pairs_from_pdf(
    pdf_path,
    source_name: str,
    language_src: str,
    language_tgt: str,
    start_page: int,
    end_page: int,
    column_gap_margin: int,
    italic_font_markers: list[str],
):
    """
    Extracts parallel pairs of Wampis and Spanish text from the
    specified page range of the PDF,
    """
    rows = []

    segment_text = ""
    segment_is_italic = None
    segment_start_page = None
    segment_end_page = None

    last_nonitalic_segment_text = None
    last_nonitalic_segment_start_page = None
    last_nonitalic_segment_end_page = None

    def finalize_current_segment():
        nonlocal segment_text, segment_is_italic, segment_start_page, segment_end_page

        nonlocal last_nonitalic_segment_text
        nonlocal last_nonitalic_segment_start_page
        nonlocal last_nonitalic_segment_end_page

        nonlocal rows

        if segment_is_italic is None:
            return

        raw_text = normalize(segment_text)
        if not raw_text:
            return

        if segment_is_italic:
            spanish = clean_spanish_text(raw_text)

            if looks_like_viable_spanish_segment(spanish) and last_nonitalic_segment_text:
                wampis = extract_last_wampis_candidate(last_nonitalic_segment_text)

                if wampis:
                    wampis = remove_embedded_page_digits_from_wampis(wampis, spanish)

                    if wampis and spanish:
                        rows.append(
                            {
                                "source": source_name,
                                language_src: wampis,
                                language_tgt: spanish,
                                "page_wampis": last_nonitalic_segment_end_page,
                                "page_spanish": segment_end_page,
                                "type": "sentence",
                                "origin": "pdf",
                            }
                        )
        else:
            last_nonitalic_segment_text = clean_wampis_text(raw_text)
            last_nonitalic_segment_start_page = segment_start_page
            last_nonitalic_segment_end_page = segment_end_page

    def process_chars(chars, current_page):
        nonlocal segment_text, segment_is_italic, segment_start_page, segment_end_page

        for ch in chars:
            ch_text = ch.get("text", "")
            if ch_text == "":
                continue

            ch_italic = is_italic(ch, italic_font_markers)

            if segment_is_italic is None:
                segment_is_italic = ch_italic
                segment_start_page = current_page
                segment_end_page = current_page
                segment_text = ch_text
                continue

            if ch_italic == segment_is_italic:
                segment_text += ch_text
                segment_end_page = current_page
            else:
                finalize_current_segment()

                segment_text = ch_text
                segment_is_italic = ch_italic
                segment_start_page = current_page
                segment_end_page = current_page

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx in range(start_page - 1, end_page):
            page = pdf.pages[page_idx]
            current_page = page_idx + 1

            mid_x = page.width / 2

            left_crop = page.crop((0, 0, mid_x - column_gap_margin, page.height))
            right_crop = page.crop((mid_x + column_gap_margin, 0, page.width, page.height))

            left_chars = dedupe_overlapped_chars(left_crop.chars)
            right_chars = dedupe_overlapped_chars(right_crop.chars)

            left_chars = sorted(
                left_chars,
                key=lambda c: (round(c.get("doctop", 0), 1), c.get("x0", 0))
            )
            right_chars = sorted(
                right_chars,
                key=lambda c: (round(c.get("doctop", 0), 1),c.get("x0", 0))
            )

            process_chars(left_chars, current_page)
            process_chars(right_chars, current_page)

    finalize_current_segment()

    rows = join_spanish_fragments(rows)

    # deduplicación exacta
    seen = set()
    deduped = []
    for row in rows:
        key = (row[language_src], row[language_tgt])
        if key not in seen:
            seen.add(key)
            deduped.append(row)

    return deduped
