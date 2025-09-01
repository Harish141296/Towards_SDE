# OCR_Book_Extractor/providers.py
from typing import List, Dict, Tuple
import requests
from rapidfuzz import process, fuzz

def google_books_search(title: str, max_results: int = 10) -> List[Dict]:
    # Public Google Books API (no key needed for basic use)
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"intitle:{title}", "maxResults": max_results}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    items = data.get("items", []) or []
    results = []
    for it in items:
        info = it.get("volumeInfo", {})
        results.append({
            "title": info.get("title"),
            "authors": info.get("authors", []),
            "publishedDate": info.get("publishedDate"),
            "infoLink": info.get("infoLink"),
            "categories": info.get("categories", []),
            "source": "google_books",
        })
    return results

def openlibrary_search(title: str, limit: int = 10) -> List[Dict]:
    url = "https://openlibrary.org/search.json"
    params = {"title": title, "limit": limit}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    docs = data.get("docs", []) or []
    results = []
    for d in docs:
        results.append({
            "title": d.get("title"),
            "authors": d.get("author_name", []),
            "publishedDate": str(d.get("first_publish_year", "")),
            "infoLink": ("https://openlibrary.org" + d.get("key", "")) if d.get("key") else None,
            "categories": [],
            "source": "openlibrary",
        })
    return results

def verify_title_against_catalogs(ocr_title: str) -> List[Dict]:
    """
    Query both catalogs and fuzzy-match returned titles to the OCR title.
    Return sorted high-confidence matches with scores.
    """
    candidates = []
    try:
        candidates.extend(google_books_search(ocr_title))
    except Exception:
        pass
    try:
        candidates.extend(openlibrary_search(ocr_title))
    except Exception:
        pass

    # Build corpus of titles to rank
    corpus = [c["title"] for c in candidates if c.get("title")]
    ranked = process.extract(
        ocr_title, corpus, scorer=fuzz.token_set_ratio, limit=10
    )
    # Attach metadata
    out = []
    for title, score, idx in ranked:
        meta = candidates[idx]
        meta = dict(meta)  # copy
        meta["score"] = score
        out.append(meta)
    # High-confidence first
    out.sort(key=lambda x: x["score"], reverse=True)
    return out
