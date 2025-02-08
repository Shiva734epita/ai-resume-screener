import json
from sqlalchemy import text
from celery import shared_task
from app.database.db_config import db
from app.services.resume_parser import parse_resume
from sqlalchemy.exc import IntegrityError
from app.services.email_service import send_email
from app import create_app 

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@shared_task(bind=True, name="app.tasks.process_resume_async")
def process_resume_async(self, filepath, user_id):
    """Background task to process resumes"""
    flask_app = create_app()
    with flask_app.app_context():
        try:
            structured_data = parse_resume(filepath)

            with db.session.begin():
                # ✅ Check if the user already uploaded the same file (user_id + filename check)
                existing_resume = db.session.execute(
                    text("SELECT id FROM resumes WHERE user_id = :user_id AND filename = :filename"),
                    {"user_id": user_id, "filename": filepath.split("/")[-1]}
                ).fetchone()

                if existing_resume:
                    print(f"⚠️ WARNING: User {user_id} already uploaded {filepath.split('/')[-1]}. Skipping insert.")
                    return {"message": "Duplicate resume detected for this user", "filename": filepath.split("/")[-1]}

                # ✅ Insert new resume into the database with `user_id`
                db.session.execute(
                    text("""
                        INSERT INTO resumes (user_id, filename, filepath, extracted_text, name, email, phone, skills, job_role)
                        VALUES (:user_id, :filename, :filepath, :extracted_text, :name, :email, :phone, :skills, :job_role)
                    """),
                    {
                        "user_id": user_id,
                        "filename": filepath.split("/")[-1],
                        "filepath": filepath,
                        "extracted_text": structured_data.get("extracted_text", ""),
                        "name": structured_data.get("name", ""),
                        "email": structured_data.get("email", ""),
                        "phone": structured_data.get("phone", ""),
                        "skills": json.dumps(structured_data.get("skills", [])),  # ✅ Store JSON properly
                        "job_role": structured_data.get("job_role", "")
                    }
                )
            
            db.session.commit()
            print(f"✅ DEBUG: Database Insert Committed for {filepath}")  

        except IntegrityError:
            db.session.rollback()  # ❌ Ensure rollback in case of errors
            print(f"❌ ERROR: Duplicate resume for user {user_id}. Skipping insert.")
            return {"message": "Duplicate resume detected.", "filename": filepath.split("/")[-1]}
        
    return {"message": "Resume processed successfully", "data": structured_data}

@shared_task(bind=True, name="app.tasks.send_otp_async")
def send_otp_async(self, email, otp, name, email_type):
    """Celery Task: Send OTP Email Asynchronously"""
    try:
        send_email(email, otp, name, email_type)
        return {"status": "success", "message": f"OTP sent to {email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
