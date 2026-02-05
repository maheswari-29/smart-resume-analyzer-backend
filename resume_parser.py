import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import docx

def extract_text_from_pdf(filepath):
    text = ""

    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() or ""
    except:
        pass

    return text.strip()


def ocr_pdf(filepath):
    images = convert_from_path(filepath)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text.strip()


def parse_resume(filepath):
    ext = filepath.split(".")[-1].lower()

    if ext == "pdf":
        text = extract_text_from_pdf(filepath)

        # OCR fallback
        if not text or len(text) < 50:
            text = ocr_pdf(filepath)

        return text

    elif ext == "docx":
        doc = docx.Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    elif ext == "txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    return ""
