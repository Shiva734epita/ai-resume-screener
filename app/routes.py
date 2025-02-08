from flask import Blueprint, request, jsonify, Flask
from app.database.db_config import db
from sqlalchemy import text
from app.controllers.resume_controller import resume_controller

routes = Blueprint("routes", __name__)

def register_routes(app: Flask):
    app.register_blueprint(resume_controller, url_prefix="/api")

@routes.route('/api/resumes', methods=['GET'])
def get_resumes():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    query = text("SELECT * FROM resumes LIMIT :limit OFFSET :offset")
    results = db.session.execute(query, {"limit": limit, "offset": (page-1)*limit}).fetchall()

    return jsonify([dict(row._asdict()) for row in results]), 200
