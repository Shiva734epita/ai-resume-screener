import pdfplumber
import docx
import os
 
UPLOAD_FOLDER = 'uploads'

def extract_text_from_pdf(filepath):
    """Uses pdfplumber to extract structured text from PDFs."""
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"ERROR: Failed to extract text from PDF: {e}")
        return ""

    return text.strip()

def extract_text_from_docx(filepath):
    """Extracts text from Word documents while preserving structure."""
    try:
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        print(f"ERROR: Failed to extract text from DOCX: {e}")
        return ""

def extract_text(filepath, file_ext):
    """Extracts structured text from PDFs and DOCX files."""
    if file_ext == "pdf":
        return extract_text_from_pdf(filepath)
    elif file_ext == "docx":
        return extract_text_from_docx(filepath)
    return ""
