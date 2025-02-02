import pdfplumber
import docx
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    """Uses pdfplumber to extract structured text from PDFs."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(filepath):
    """Extracts text from Word documents while preserving structure."""
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_text(filepath, file_ext):
    """Extracts structured text from PDFs and DOCX files."""
    if file_ext == "pdf":
        return extract_text_from_pdf(filepath)
    elif file_ext == "docx":
        return extract_text_from_docx(filepath)
    return ""
