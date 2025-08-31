import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Harish\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
from PIL import Image
import cv2
import sys

def extract_text(image_path: str) -> str:
    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Optional: Thresholding for better OCR
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Run OCR
    text = pytesseract.image_to_string(thresh)

    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path>")
    else:
        img_path = sys.argv[1]
        extracted = extract_text(img_path)
        print("\n--- Extracted Text ---\n")
        print(extracted)
