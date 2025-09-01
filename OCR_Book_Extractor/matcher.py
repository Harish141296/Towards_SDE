# OCR_Book_Extractor/matcher.py
import re
from typing import List, Dict, Tuple
from rapidfuzz import process, fuzz

TITLE_MIN_LEN = 3
TITLE_MAX_LEN = 120

# Basic cleanup: remove emojis, URLs, extra spaces, instagram cruft
EMOJI_PATTERN = re.compile(
    "["                       # emoji block
    "\U0001F600-\U0001F64F"   # emoticons
    "\U0001F300-\U0001F5FF"   # symbols & pictographs
    "\U0001F680-\U0001F6FF"   # transport & map
    "\U0001F1E0-\U0001F1FF"   # flags
    "]+", flags=re.UNICODE
)
URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)")
HANDLE_PATTERN = re.compile(r"@\w+")
HASH_PATTERN = re.compile(r"#\w+")
MULTISPACE = re.compile(r"\s+")

def clean_text(raw: str) -> str:
    t = raw
    t = EMOJI_PATTERN.sub(" ", t)
    t = URL_PATTERN.sub(" ", t)
    t = HANDLE_PATTERN.sub(" ", t)
    t = HASH_PATTERN.sub(" ", t)
    t = t.replace("•", " ").replace("|", " ").replace("—", " ")
    t = MULTISPACE.sub(" ", t)
    return t.strip()

def candidate_lines(cleaned: str) -> List[str]:
    """
    Heuristic: titles often appear as:
    - Title case lines (Many Words Capitalized)
    - Quoted lines
    - Bullet-like short lines
    - Lines with separator removed but still reasonably short
    """
    lines = [ln.strip() for ln in re.split(r"[\r\n]", cleaned)]
    # Also split on common separators that might have been inline
    split_more = []
    for ln in lines:
        split_more.extend(re.split(r"\s[-–—]\s|\s•\s| · ", ln))
    lines = [ln.strip() for ln in split_more if ln.strip()]

    candidates = []
    for ln in lines:
        if not (TITLE_MIN_LEN <= len(ln) <= TITLE_MAX_LEN):
            continue
        # Filter obvious non-titles: mostly digits/symbols
        alpha_ratio = sum(c.isalpha() for c in ln) / max(1, len(ln))
        if alpha_ratio < 0.5:
            continue
        # Prefer lines that look like titles: title case or quoted
        looks_titled = (
            ln.startswith(("'", '"')) and ln.endswith(("'", '"'))
            or sum(w[:1].isupper() for w in ln.split()) >= max(2, len(ln.split()) // 2)
        )
        # Also accept concise lines with 3–12 words
        word_count = len(ln.split())
        if looks_titled or 3 <= word_count <= 12:
            candidates.append(ln.strip('"\''))

    # De-duplicate while preserving order
    seen = set()
    uniq = []
    for c in candidates:
        k = c.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    return uniq

def fuzzy_pick_best(
    query: str, choices: List[str], limit: int = 5, score_cutoff: int = 80
) -> List[Tuple[str, int]]:
    """
    Return top matches (choice, score) for query from choices.
    Uses token_set_ratio to reduce word-order sensitivity.
    """
    return process.extract(
        query,
        choices,
        scorer=fuzz.token_set_ratio,
        limit=limit,
        score_cutoff=score_cutoff
    )

def select_titles_from_ocr(raw_text: str) -> List[str]:
    """
    Main entry: raw OCR -> cleaned -> candidates
    (Verification against real catalogs happens in providers.py)
    """
    cleaned = clean_text(raw_text)
    return candidate_lines(cleaned)
