from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.database.db_config import db
from app.utils.config import Config

def create_app():
    """Flask Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database & Migrations
    db.init_app(app)
    migrate = Migrate(app, db)

    # Import Blueprints inside function to avoid circular imports
    with app.app_context():
        from app.controllers.resume_controller import resume_controller
        app.register_blueprint(resume_controller, url_prefix="/api")

    return app
