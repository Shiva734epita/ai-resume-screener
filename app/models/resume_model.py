from app.database.db_config import db
from sqlalchemy import Index

class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True, index=True)
    phone = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.JSON, nullable=True)  
    job_role = db.Column(db.String(255), nullable=True, index=True)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)

    # ✅ Define relationship here after both models are defined
    user = db.relationship("User", back_populates="user_resumes", lazy=True)

    def __init__(self, user_id, filename, filepath, extracted_text, name, email, phone, skills, job_role):
        self.user_id = user_id
        self.filename = filename
        self.filepath = filepath
        self.extracted_text = extracted_text
        self.name = name
        self.email = email
        self.phone = phone
        self.skills = skills
        self.job_role = job_role

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "filepath": self.filepath,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "job_role": self.job_role,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }

# ✅ Indexes for performance
__table_args__ = (
    Index("idx_email", Resume.email),
    Index("idx_job_role", Resume.job_role),
    Index("idx_user_id", Resume.user_id),
    Index("idx_uploaded_at", Resume.uploaded_at),
)
