# OCR_Book_Extractor/main.py
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Harish\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
from matcher import select_titles_from_ocr
from providers import verify_title_against_catalogs
from PIL import Image
import cv2
import sys

# if tesseract is not on PATH, uncomment and set:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def preprocess_image(image_path):
    # Load image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize for better OCR
    scale_percent = 200
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    gray = cv2.resize(gray, (width, height))

    # Denoise
    gray = cv2.medianBlur(gray, 3)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    # Invert if text is white on dark
    thresh = cv2.bitwise_not(thresh)

    return thresh

def extract_text(image_path: str) -> str:
    processed = preprocess_image(image_path)
    texts = []
    for psm in [3, 6, 11]:
        config = f"--psm {psm}"
        text = pytesseract.image_to_string(processed, config=config)
        texts.append(text.strip())
        
    return text

def run_pipeline(image_path: str):
    raw = extract_text(image_path)
    print("\n--- RAW OCR (truncated) ---\n", raw[:500], "...\n")

    candidates = select_titles_from_ocr(raw)
    print("--- CANDIDATE TITLES (heuristics) ---")
    for c in candidates[:10]:
        print(" •", c)

    print("\n--- VERIFIED (Google Books/OpenLibrary) ---")
    for c in candidates[:5]:  # Verify top-5 candidates to save calls
        hits = verify_title_against_catalogs(c)
        best = [h for h in hits if h["score"] >= 80][:3]
        if best:
            print(f"\nOCR: {c}")
            for h in best:
                print(f"  -> [{h['score']}] {h['title']} — {', '.join(h['authors'] or [])} ({h['source']})")
                print(f"     info: {h['infoLink']}")
        else:
            print(f"\nOCR: {c}")
            print("  -> no high-confidence matches yet")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py <image_path>")
        sys.exit(1)
    run_pipeline(sys.argv[1])
