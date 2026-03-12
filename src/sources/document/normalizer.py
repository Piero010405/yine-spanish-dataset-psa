"""
Normalizer utilities for document-based bilingual extraction.
"""

import re


def normalize(text: str) -> str:
    """
    Normalizes the input text by replacing newlines with spaces, collapsing multiple
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def ends_with_final_punctuation(text: str) -> bool:
    """
    Ends with a final punctuation mark that typically indicates the 
    end of a sentence in Spanish.
    """
    text = normalize(text)
    return bool(re.search(r"[.!?…]$", text))


def starts_like_continuation(text: str) -> bool:
    """
    Starts with a lowercase letter or common Spanish
    conjunctions/prepositions that often indicate a continuation of a sentence.
    """
    text = normalize(text)
    if not text:
        return False

    if re.match(r"^[a-záéíóúñü]", text):
        return True

    continuation_starts = [
        "a ", "al ", "del ", "de ", "con ", "por ", "para ", "y ", "e ",
        "o ", "u ", "que ", "como ", "cuando ", "donde ", "en ", "sin ",
        "sobre ", "entre ", "hasta ", "desde "
    ]

    lowered = text.lower()
    return any(lowered.startswith(x) for x in continuation_starts)


def ends_like_incomplete_spanish(text: str) -> bool:
    """
    Ends with a word that is commonly found at the end of incomplete Spanish sentences
    """
    text = normalize(text)
    if not text:
        return False

    if ends_with_final_punctuation(text):
        return False

    trailing_tokens = {
        "a", "al", "del", "de", "con", "por", "para", "y", "e", "o", "u",
        "el", "la", "los", "las", "un", "una", "unos", "unas",
        "mi", "tu", "su", "sus", "mis", "tus",
        "este", "esta", "estos", "estas",
        "ese", "esa", "esos", "esas",
        "aquí", "aca", "acá", "ahí", "alli", "allí",
        "voy", "va", "vamos", "van"
    }

    words = text.lower().split()
    if not words:
        return False

    last_word = re.sub(r"[^\wáéíóúñü]", "", words[-1])

    if last_word in trailing_tokens:
        return True

    if len(words) <= 4:
        return True

    last_two = " ".join(words[-2:]) if len(words) >= 2 else ""
    suspicious_bigrams = {
        "voy a", "va a", "vamos a", "van a",
        "queda mi", "queda su", "queda tu",
        "alcanzame el", "alcánzame el",
        "aprende a", "enseña a", "enséñale a"
    }

    return last_two in suspicious_bigrams


def join_spanish_fragments(rows):
    """
    Joins consecutive rows of the dataset where the Spanish text
    appears to be split across multiple rows
    """
    if not rows:
        return rows

    merged = []
    i = 0

    while i < len(rows):
        current = dict(rows[i])

        while i + 1 < len(rows):
            nxt = rows[i + 1]

            current_spanish = normalize(current["spanish"])
            next_spanish = normalize(nxt["spanish"])

            same_source = current["source"] == nxt["source"]
            close_pages = (
                nxt["page_spanish"] == current["page_spanish"]
                or nxt["page_spanish"] == current["page_spanish"] + 1
            )

            should_merge = (
                same_source
                and close_pages
                and ends_like_incomplete_spanish(current_spanish)
                and starts_like_continuation(next_spanish)
            )

            if not should_merge:
                break

            current["spanish"] = normalize(current_spanish + " " + next_spanish)
            current["page_spanish"] = nxt["page_spanish"]
            i += 1

        merged.append(current)
        i += 1

    return merged


def has_letters(text: str) -> bool:
    """
    Has at least one letter
    """
    return bool(re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü]", text))


def has_digits(text: str) -> bool:
    """
    Has at least one digit
    """
    return bool(re.search(r"\d", text))


def clean_wampis_text(text: str) -> str:
    """
    Cleans the Wampis text by removing leading digits, trimming whitespace
    """
    text = normalize(text)
    text = text.lstrip("0123456789 ").strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text.strip()


def clean_spanish_text(text: str) -> str:
    """
    Cleans the Spanish text by normalizing it and removing
    leading punctuation that is not followed by a letter or digit
    """
    text = normalize(text)
    text = re.sub(r"^[\s\.,;:!?¡¿]+(?=[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9])", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text.strip()


def remove_embedded_page_digits_from_wampis(wampis: str, spanish: str) -> str:
    """
    Removes embedded page numbers from the Wampis text if the Spanish text contains digits
    """
    if has_digits(spanish):
        return normalize(wampis)

    text = wampis
    text = re.sub(r"(?<=[A-Za-zÁÉÍÓÚáéíóúÑñÜü])\d{1,3}(?=[A-Za-zÁÉÍÓÚáéíóúÑñÜü])", "", text)
    text = re.sub(r"(?<=\s)\d{1,3}(?=[A-Za-zÁÉÍÓÚáéíóúÑñÜü])", "", text)
    text = re.sub(r"(?<=[A-Za-zÁÉÍÓÚáéíóúÑñÜü])\d{1,3}(?=\s)", "", text)
    text = re.sub(r"\b\d{1,3}\b", " ", text)
    text = normalize(text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text.strip()


def split_into_sentence_like_chunks(text: str):
    """
    Splits the text into chunks that resemble sentences based on punctuation marks.
    """
    text = normalize(text)
    if not text:
        return []

    chunks = []
    buffer = []

    i = 0
    n = len(text)

    while i < n:
        ch = text[i]
        buffer.append(ch)

        if ch in ".!?…":
            j = i + 1
            while j < n and text[j] in ".!?…":
                buffer.append(text[j])
                j += 1

            chunk = "".join(buffer).strip()
            if chunk:
                chunks.append(chunk)
            buffer = []
            i = j
            continue

        i += 1

    tail = "".join(buffer).strip()
    if tail:
        chunks.append(tail)

    return [normalize(c) for c in chunks if normalize(c)]


def looks_like_metadata_or_definition(text: str) -> bool:
    """
    Looks like metadata or a definition based on the presence of certain abbreviations
    """
    t = normalize(text)

    pos_patterns = [
        r"\badv\.",
        r"\badj\.",
        r"\binterj\.",
        r"\bpron\.",
        r"\bs\.",
        r"\bv\.",
        r"\bnum\.",
        r"\bnec\.",
    ]

    for pat in pos_patterns:
        if re.search(pat, t, flags=re.IGNORECASE):
            return True

    if re.search(r"\(expresión.*?\)", t, flags=re.IGNORECASE):
        return True

    if t.count(",") >= 2 and not re.search(r"[.!?…]$", t):
        return True

    return False


def starts_like_sentence(text: str) -> bool:
    """
    Starts like a sentence based on starting with an
    uppercase letter or an opening punctuation followed by an uppercase letter
    """
    t = normalize(text)
    if not t:
        return False

    if re.match(r"^[A-ZÁÉÍÓÚÑÜ]", t):
        return True
    if re.match(r"^[¡¿][A-ZÁÉÍÓÚÑÜ]", t):
        return True

    return False


def looks_like_viable_wampis_candidate(text: str) -> bool:
    """
    Looks like a viable Wampis candidate based on length, presence of letters, and word count
    """
    t = clean_wampis_text(text)

    if len(t) < 8:
        return False
    if not has_letters(t):
        return False
    if len(t.split()) < 2:
        return False

    return True


def extract_last_wampis_candidate(nonitalic_text: str) -> str | None:
    """
    Extracts the last viable Wampis candidate from the given
    non-italic text by splitting it into
    """
    text = clean_wampis_text(nonitalic_text)
    if not text:
        return None

    chunks = split_into_sentence_like_chunks(text)
    if not chunks:
        return None

    cleaned_chunks = []
    for c in chunks:
        c = clean_wampis_text(c)
        if looks_like_viable_wampis_candidate(c):
            cleaned_chunks.append(c)

    if not cleaned_chunks:
        return None

    for c in reversed(cleaned_chunks):
        if starts_like_sentence(c) and not looks_like_metadata_or_definition(c):
            return c

    for c in reversed(cleaned_chunks):
        if not looks_like_metadata_or_definition(c):
            return c

    return cleaned_chunks[-1]


def looks_like_viable_spanish_segment(text: str) -> bool:
    """
    Looks like a viable Spanish segment based on length, presence of letters, and word count
    """
    t = clean_spanish_text(text)

    if len(t) < 6:
        return False
    if not has_letters(t):
        return False
    if len(t.split()) < 2:
        return False

    return True
