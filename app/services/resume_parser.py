import re
import spacy
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import fitz 
import numpy as np

nlp = spacy.load("en_core_web_lg")
# Load skill and job title databases
BASE_DIR = os.path.dirname(__file__)
SKILLS_DB_PATH = os.path.join(BASE_DIR, "../data/skills.json")
JOB_TITLES_DB_PATH = os.path.join(BASE_DIR, "../data/job_titles.json")

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return {}

SKILL_DATABASE = load_json(SKILLS_DB_PATH)
JOB_TITLE_MAPPING = load_json(JOB_TITLES_DB_PATH)

with open("app/data/job_titles.json", "r") as f:
    job_titles = json.load(f)

# ✅ Fix case where job_titles is incorrectly loaded as a dictionary
if isinstance(job_titles, dict):  
    job_titles = list(job_titles.values())  

# ✅ Ensure all job titles are strings (not lists or objects)
job_titles = [str(title) for title in job_titles]  

def extract_text_from_pdf(pdf_path):
    """ Extracts raw text from a PDF file. """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text("text") + " "

    return full_text.strip()

def extract_name_ner(text):
    """ Extracts the first valid PERSON entity using NER. """
    nlp_doc = nlp(text)
    person_names = [ent.text.strip() for ent in nlp_doc.ents if ent.label_ == "PERSON"]

    if person_names:
        return person_names[0]  # Return the first valid name found

    return None  # Return None if no valid name is found

def extract_name_regex(text):
    """ Extracts the name using Regex if 'Name:' label is present. """
    name_pattern = r"Name:\s*([A-Za-z\s]+)"
    match = re.search(name_pattern, text)

    return match.group(1).strip() if match else None  # Return None if no match

def extract_name_top_lines(text):
    """ Extracts the first valid text assuming it's a name. """
    lines = text.split("\n")
    
    for line in lines:
        words = line.strip().split()
        if 2 <= len(words) <= 4:  # Likely a name (First + Last Name)
            return line.strip()
    
    return None  # Return None if no valid name is found

def extract_name(pdf_path):
    """ Hybrid method: Try Regex → NER → Top-Line Extraction. """
    text = extract_text_from_pdf(pdf_path)

    # Try regex first
    name = extract_name_regex(text)
    if name:
        return name

    # Try Named Entity Recognition (NER)
    name = extract_name_ner(text)
    if name:
        return name

    # Try extracting from top lines as a fallback
    name = extract_name_top_lines(text)
    return name if name else "Name not found"

def extract_email(resume_text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text)
    return match.group(0) if match else "Unknown"

def extract_phone(text):
    """Extract phone number from resume text"""
    phone_pattern = re.compile(r'\+?\d[\d\s\-\(\)]{8,}')  # ✅ Supports multiple phone formats
    match = phone_pattern.search(text)
    return match.group() if match else "Unknown"

def extract_skills(resume_text):
    """Returns skills as a JSONB-compatible dictionary."""
    found_skills = {}
    for category, skills in SKILL_DATABASE.items():
        found_skills[category] = [skill for skill in skills if skill.lower() in resume_text.lower()]
    return found_skills  # ✅ Now structured as a JSON object

vectorizer = TfidfVectorizer().fit(job_titles)
job_vectors = vectorizer.transform(job_titles)

def extract_job_role(text):
    """Uses AI-powered text similarity to detect job role"""
    text_vector = vectorizer.transform([text])  # Convert resume text into numerical features
    similarities = np.dot(job_vectors, text_vector.T).toarray().flatten()  # Compute similarity scores

    if np.all(similarities == 0):  # ✅ Handle case where no job role is matched
        return "Unknown"

    best_match_idx = int(np.argmax(similarities))  # ✅ Convert NumPy index to Python int
    best_match = job_titles[best_match_idx]  # ✅ Get best-matching job role

    if similarities[best_match_idx] > 0.2:  # ✅ Confidence threshold
        return best_match  # ✅ Return as a clean string

    return "Unknown" 

def parse_resume(filepath):
    """Extract structured information from resume text"""
    
    resume_text = extract_text_from_pdf(filepath)  # ✅ Use new PDF extraction method

    print(f"DEBUG: Clean Resume Text:\n{resume_text[:1000]}")  # ✅ Print first 1000 characters

    structured_data = {
        "name": extract_name(filepath),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "skills": extract_skills(resume_text),
        "job_role": extract_job_role(resume_text),
    }

    print(f"DEBUG: Extracted Data:\n{structured_data}")  # ✅ Log structured data

    return structured_data


# def extract_text(filepath, file_ext):
#     """Extracts structured text from PDFs and DOCX files."""
#     if file_ext == "pdf":
#         return extract_text_from_pdf(filepath)
#     elif file_ext == "docx":
#         return extract_text_from_docx(filepath)
#     return ""