import re
import spacy
import json
import os

nlp = spacy.load("en_core_web_sm")

# Load skills and job titles from JSON
SKILLS_DB_PATH = os.path.join(os.path.dirname(__file__), "../data/skills.json")
JOB_TITLES_DB_PATH = os.path.join(os.path.dirname(__file__), "../data/job_titles.json")

def load_skills():
    """Loads skills dynamically from a JSON file"""
    if not os.path.exists(SKILLS_DB_PATH):
        return set()
    
    with open(SKILLS_DB_PATH, "r") as file:
        skills_data = json.load(file)

    skill_set = set()
    for category, skills in skills_data.items():
        skill_set.update(skills)
    return skill_set

def load_job_titles():
    """Loads job titles dynamically from a JSON file"""
    if not os.path.exists(JOB_TITLES_DB_PATH):
        return {}

    with open(JOB_TITLES_DB_PATH, "r") as file:
        return json.load(file)

# ✅ Initialize skill database and job title mapping
SKILL_DATABASE = load_skills()
JOB_TITLE_MAPPING = load_job_titles()

def extract_name(resume_text):
    """Extracts name from the resume while ensuring job roles are not attached."""
    doc = nlp(resume_text)
    person_entities = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]

    if not person_entities:
        return "Unknown"

    # Split name and job title if attached
    full_person_entry = person_entities[0]
    split_text = full_person_entry.split("\n")
    actual_name = split_text[0].strip()

    print(f"DEBUG: Extracted Name: {actual_name}")
    return actual_name

def extract_email(resume_text):
    """Extract email using regex"""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.findall(email_pattern, resume_text)
    return match[0].strip() if match else "Not found"

def extract_phone(resume_text):
    """Extract phone number using regex"""
    phone_pattern = r"\(?\+?\d{1,3}\)?[-.\s]?\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}"
    match = re.findall(phone_pattern, resume_text)
    return match[0].strip() if match else "Not found"

def extract_skills(resume_text):
    """Extract skills dynamically from the loaded skills database"""
    doc = nlp(resume_text)
    extracted_skills = set()

    for token in doc:
        if token.text in SKILL_DATABASE:
            extracted_skills.add(token.text)

    return list(extracted_skills) if extracted_skills else ["Not specified"]

def normalize_job_role(job_role):
    """Maps extracted job role to a standardized title using job_titles.json"""
    job_role_cleaned = job_role.strip().lower()

    for standard_title, variations in JOB_TITLE_MAPPING.items():
        if job_role_cleaned in [v.lower() for v in variations]:
            return standard_title
    
    return job_role if len(job_role.split()) > 1 else "Unknown"

def extract_job_role(resume_text):
    """Extracts job role using structured section scanning and NLP keyword matching."""
    doc = nlp(resume_text)
    job_titles = []

    person_name = extract_name(resume_text)
    JOB_KEYWORDS = ["Engineer", "Developer", "Analyst", "Consultant", "Manager",
                    "Scientist", "Specialist", "Architect", "Lead", "Intern"]

    EXPERIENCE_SECTIONS = ["Work Experience", "Professional Experience", "Employment History"]
    PROJECT_SECTIONS = ["Projects", "Personal Projects", "Academic Projects"]

    print("\n🔍 DEBUG: NLP Detected Entities:")
    for ent in doc.ents:
        print(f"Entity: {ent.text} | Label: {ent.label_}")

    detected_role = None
    for section in EXPERIENCE_SECTIONS + PROJECT_SECTIONS:
        if section in resume_text:
            extracted_section = resume_text.split(section, 1)[-1][:500]
            print(f"DEBUG: Extracting Job Role from {section} section: {extracted_section}")

            for word in extracted_section.split():
                if word in JOB_KEYWORDS:
                    detected_role = word
                    break

    if not detected_role:
        past_roles = []
        for ent in doc.ents:
            if ent.label_ in ["ORG", "TITLE"] and any(word in ent.text.split() for word in JOB_KEYWORDS):
                past_roles.append(ent.text.strip())

        if past_roles:
            past_roles = sorted(past_roles, key=lambda x: len(x.split()), reverse=True)
            detected_role = past_roles[0]

    detected_role = detected_role if detected_role else "Unknown"

    if person_name in detected_role:
        detected_role = detected_role.replace(person_name, "").strip()

    if not detected_role.strip():
        detected_role = "Unknown"

    detected_role = normalize_job_role(detected_role)
    print("DEBUG: Final Job Role After Normalization:", detected_role)
    return detected_role

def validate_resume_data(data):
    """Validate and clean extracted resume data"""
    return {
        "name": data["name"] if data["name"] else "Unknown",
        "email": data["email"] if data["email"] else "Not found",
        "phone": data["phone"] if data["phone"] else "Not found",
        "skills": ", ".join(data["skills"]) if data["skills"] else "Not specified",
        "job_role": data["job_role"] if data["job_role"] else "Unknown"
    }

def parse_resume(resume_text):
    """Run all parsers and validate extracted resume data"""
    extracted_data = {
        "name": extract_name(resume_text),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "skills": extract_skills(resume_text),
        "job_role": extract_job_role(resume_text)
    }
    return validate_resume_data(extracted_data)
