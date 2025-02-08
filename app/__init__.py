from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery
from app.database.db_config import db
from app.utils.config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

celery = Celery()  # ✅ Initialize Celery globally
jwt = JWTManager() 

def create_app():
    """Flask Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"DEBUG: JWT_SECRET_KEY -> {app.config.get('JWT_SECRET_KEY')}")

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # ✅ Ensure Celery configuration is loaded
    app.config.update(
        CELERY_BROKER_URL="redis://localhost:6380/0",
        RESULT_BACKEND="redis://localhost:6380/0"
    )

    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)

    with app.app_context():
        from app.controllers import resume_controller  
        app.register_blueprint(resume_controller.resume_controller, url_prefix="/api")
        from app.controllers.auth_controller import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/api")

    # ✅ Bind Flask app to Celery
    celery.conf.update(app.config)
    
    return app
