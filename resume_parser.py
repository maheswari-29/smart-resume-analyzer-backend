import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def parse_resume(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    if ext == ".pdf":
        # 1️⃣ Try normal text extraction
        text = extract_text_from_pdf(filepath)
        if text and len(text.strip()) > 50:
            return text

        # 2️⃣ Fallback to OCR (for scanned PDFs)
        return extract_text_with_ocr(filepath)

    return ""


def extract_text_from_pdf(filepath):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass

    return text


def extract_text_with_ocr(filepath):
    text = ""
    try:
        images = convert_from_path(filepath, dpi=300)
        for img in images:
            text += pytesseract.image_to_string(
                img,
                config="--psm 6"
            )
    except Exception as e:
        print("OCR ERROR:", e)

    return text
