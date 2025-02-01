import os

DATABASE_URL = "postgresql://muralikrish:Levika123@localhost:5432/ai_resume_dev"

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
