import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = "postgresql://muralikrish:Levika123@localhost:5432/ai_resume_dev"

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_super_secure_secret") 
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour expiration
