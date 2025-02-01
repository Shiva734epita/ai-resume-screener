import re
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

def extract_name(resume_text):
    """Extract name from resume using NLP"""
    doc = nlp(resume_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"

def extract_email(resume_text):
    """Extract email using regex"""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.findall(email_pattern, resume_text)
    return match[0] if match else "Not found"

def extract_phone(resume_text):
    """Extract phone number using regex"""
    phone_pattern = r"\(?\+?\d{1,3}\)?[-.\s]?\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}"
    match = re.findall(phone_pattern, resume_text)
    return match[0] if match else "Not found"

def extract_skills(resume_text):
    """Extract skills from predefined skillset"""
    skillset = {"Python", "Java", "SQL", "Machine Learning", "Deep Learning", "Data Science",
                "Flask", "Django", "REST API", "Docker", "Kubernetes", "AWS", "React", "Node.js"}
    
    words = set(resume_text.split())
    found_skills = list(skillset.intersection(words))
    return found_skills if found_skills else ["Not found"]

def parse_resume(resume_text):
    """Run all parsers and return structured resume data"""
    return {
        "name": extract_name(resume_text),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "skills": extract_skills(resume_text)
    }
