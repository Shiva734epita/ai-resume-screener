from app.database.db_config import db
from datetime import datetime

class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, filename, filepath, extracted_text, name, email, phone, skills):
        self.filename = filename
        self.filepath = filepath
        self.extracted_text = extracted_text
        self.name = name
        self.email = email
        self.phone = phone
        self.skills = skills
