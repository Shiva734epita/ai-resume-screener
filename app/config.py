import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_super_secure_secret") 
    JWT_ACCESS_TOKEN_EXPIRES = 3600 
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ai_resume_dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6380/0") 
    RESULT_BACKEND = os.getenv("RESULT_BACKEND", "redis://localhost:6380/0") 

