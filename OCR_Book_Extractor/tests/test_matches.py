# OCR_Book_Extractor/tests/test_matcher.py
from matcher import clean_text, candidate_lines

def test_clean_basic():
    raw = "📚 The Alchemist — Paulo Coelho #books https://example.com"
    t = clean_text(raw)
    assert "Alchemist" in t
    assert "http" not in t
    assert "#" not in t

def test_candidates():
    raw = "Must Read:\nThe Alchemist\nAtomic Habits\nSome random 1234 @$%"
    t = clean_text(raw)
    cands = candidate_lines(t)
    assert "The Alchemist" in cands
    assert "Atomic Habits" in cands
