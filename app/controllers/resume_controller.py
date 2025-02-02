from flask import Blueprint, json, request, jsonify  
import os
import re 
import spacy 
from werkzeug.utils import secure_filename
from sqlalchemy import text
from app.database.db_config import db
from app.services.resume_service import extract_text, allowed_file, UPLOAD_FOLDER
from app.services.resume_parser import parse_resume

nlp = spacy.load("en_core_web_sm") 

resume_controller = Blueprint("resume_controller", __name__)

@resume_controller.route('/get-resumes', methods=['GET'])
def get_resumes():
    """Retrieve all saved resumes from the database"""
    print("\n🔍 DEBUG: Received request on /get-resumes")

    try:
        result = db.session.execute(text("SELECT id, filename, name, email, phone, skills, job_role FROM resumes ORDER BY id DESC"))
        resumes = [dict(row) for row in result.mappings()]
        return jsonify({"resumes": resumes}), 200

    except Exception as e:
        print("❌ ERROR: Failed to fetch resumes:", e)
        return jsonify({"error": "Database error", "details": str(e)}), 500

@resume_controller.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file uploads and store structured data in the database"""
    print("\n🔍 DEBUG: Received request on /upload-resume")

    if 'file' not in request.files:
        print("❌ ERROR: No file part in request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        print("❌ ERROR: No selected file")
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        print(f"✅ File saved at: {filepath}")

        file_ext = filename.rsplit('.', 1)[1].lower()
        extracted_text = extract_text(filepath, file_ext)
        structured_data = parse_resume(extracted_text)

        print("✅ DEBUG: Extracted Resume Data:", structured_data)

        # Insert data into database
        try:
            with db.session.begin():
                db.session.execute(
                    text("INSERT INTO resumes (filename, filepath, extracted_text, name, email, phone, skills, job_role) "
                         "VALUES (:filename, :filepath, :extracted_text, :name, :email, :phone, :skills, :job_role)"),
                    {
                        "filename": filename,
                        "filepath": filepath,
                        "extracted_text": extracted_text,
                        "name": structured_data["name"],
                        "email": structured_data["email"],
                        "phone": structured_data["phone"],
                        "skills": structured_data["skills"],
                        "job_role": structured_data["job_role"]
                    }
                )
                db.session.commit()
                print("✅ DEBUG: Data inserted successfully into DB!")
        except Exception as e:
            print("❌ ERROR: Database Insert Failed:", e)
            db.session.rollback()
            return jsonify({"error": "Database error", "details": str(e)}), 500

        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "structured_data": structured_data
        }), 200
    else:
        print("❌ ERROR: Invalid file type")
        return jsonify({"error": "Invalid file type. Only PDF and DOCX are allowed."}), 400


@resume_controller.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Resume Controller is Working!"})


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

    # Step 1: Extract job roles from structured resume sections
    for section in EXPERIENCE_SECTIONS + PROJECT_SECTIONS:
        if section in resume_text:
            extracted_section = resume_text.split(section, 1)[-1][:500]
            print(f"DEBUG: Extracting Job Role from {section} section: {extracted_section}")

            # Capture multi-word job titles
            job_title_pattern = r"(?i)([A-Za-z\s]+?(Engineer|Developer|Analyst|Consultant|Manager|Scientist|Specialist|Architect|Lead|Intern))"
            match = re.search(job_title_pattern, extracted_section)

            if match:
                detected_role = match.group(1).strip()
                print(f"DEBUG: Regex Job Role Found: {detected_role}")

    # Step 2: If no role is found, scan NLP-detected entities
    if not detected_role:
        for ent in doc.ents:
            if ent.label_ in ["ORG", "TITLE"] and any(word in ent.text.split() for word in JOB_KEYWORDS):
                job_titles.append(ent.text.strip())

        if job_titles:
            job_titles = sorted(job_titles, key=lambda x: len(x.split()), reverse=True)
            detected_role = job_titles[0]
            print(f"DEBUG: NLP Job Role Found: {detected_role}")

    detected_role = detected_role if detected_role else "Unknown"

    # Step 3: Ensure the job role does not contain the extracted name
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
