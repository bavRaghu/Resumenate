import os
from pdfminer.high_level import extract_text as extract_text_from_pdf
import docx2txt

def extract_text_from_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")

    if file_path.lower().endswith(".pdf"):
        try:
            return extract_text_from_pdf(file_path).strip()
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {e}")

    elif file_path.lower().endswith(".docx"):
        try:
            return docx2txt.process(file_path).strip()
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from DOCX: {e}")

    else:
        raise ValueError("Unsupported file format. Please upload a .pdf or .docx file.")


