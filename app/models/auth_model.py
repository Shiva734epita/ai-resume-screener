from app.database.db_config import db

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    legal_details = db.Column(db.JSON, nullable=False)  
    role = db.Column(db.String(50), nullable=False, default="user")  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_resumes = db.relationship("Resume", back_populates="user", lazy=True)

    def __init__(self, email, password_hash, full_name, legal_details, role="user"):
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.legal_details = legal_details
        self.role = role

    def serialize(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "legal_details": self.legal_details,  
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class OTPStore(db.Model):
    __tablename__ = "otp_store"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
