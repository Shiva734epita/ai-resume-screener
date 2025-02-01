import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import text
from app.database.db_config import db
from app.services.resume_service import extract_text, allowed_file, UPLOAD_FOLDER
from app.services.resume_parser import parse_resume

resume_controller = Blueprint("resume_controller", __name__)

@resume_controller.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract text
        file_ext = filename.rsplit('.', 1)[1].lower()
        extracted_text = extract_text(filepath, file_ext)

        # Parse structured resume data
        structured_data = parse_resume(extracted_text)

        # Debugging Print
        print("DEBUG: Saving to database - Filename:", filename)
        print("DEBUG: Extracted Data:", structured_data)
        
        try:
            with db.session.begin():
                db.session.execute(
                    text("INSERT INTO resumes (filename, filepath, extracted_text, name, email, phone, skills) VALUES (:filename, :filepath, :extracted_text, :name, :email, :phone, :skills)"),
                    {
                        "filename": filename,
                        "filepath": filepath,
                        "extracted_text": extracted_text,
                        "name": structured_data["name"],
                        "email": structured_data["email"],
                        "phone": structured_data["phone"],
                        "skills": ", ".join(structured_data["skills"])
                    }
                )
                print("DEBUG: Data inserted successfully!")
        except Exception as e:
            print("ERROR: Database Insert Failed:", e)
            db.session.rollback()
            return jsonify({"error": "Database error"}), 500
        
        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "structured_data": structured_data
        }), 200
    else:
        return jsonify({"error": "Invalid file type. Only PDF and DOCX are allowed."}), 400
    
@resume_controller.route('/get-resumes', methods=['GET'])
def get_resumes():
    """Fetch all resumes from the database"""
    try:
        query = text("SELECT id, filename, email, phone, skills, uploaded_at FROM resumes ORDER BY uploaded_at DESC")
        result = db.session.execute(query)
        resumes = [
            {
                "id": row.id,
                "filename": row.filename,
                "email": row.email,
                "phone": row.phone,
                "skills": row.skills.split(", ") if row.skills else [],
                "uploaded_at": row.uploaded_at
            }
            for row in result
        ]
        return jsonify(resumes), 200
    except Exception as e:
        print("ERROR: Failed to fetch resumes:", e)
        return jsonify({"error": "Database query failed"}), 500

