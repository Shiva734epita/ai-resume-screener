from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.database.db_config import db
from app.utils.config import Config

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import Blueprints and Register Routes
from app.controllers.resume_controller import resume_controller
app.register_blueprint(resume_controller)
