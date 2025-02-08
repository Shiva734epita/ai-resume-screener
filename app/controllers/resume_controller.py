from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.database.db_config import db
from sqlalchemy import text
import app.services.auth_service as auth_service
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.resume_model import Resume

resume_controller = Blueprint("resume_controller", __name__)

UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@resume_controller.route('/upload-resume', methods=['POST'])
def upload_resume():
    from app.tasks import process_resume_async, allowed_file
    
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    token = token.split(" ")[1]  # Extract the actual token
    user_data = auth_service.verify_token(token)

    if not user_data:
        return jsonify({"error": "Invalid token"}), 401

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # ✅ Extract user_id correctly
    user_id = user_data.get("user_id")

    # ✅ Send task to Celery (No DB insert here)
    task = process_resume_async.apply_async(args=[filepath, user_id], queue="celery")

    return jsonify({
        "message": "File uploaded successfully",
        "task_id": task.id
    }), 202

@resume_controller.route("/resumes", methods=["GET"])
def get_resumes():
    """Fetch all resumes uploaded by the authenticated user (Excludes extracted_text)"""
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    token = token.split(" ")[1]  # Extract the actual token
    user_data = auth_service.verify_token(token)

    if not user_data:
        return jsonify({"error": "Invalid token"}), 401

    # ✅ Ensure token structure is decoded correctly
    identity = user_data

    if isinstance(identity, str):
        identity = json.loads(identity)  # ✅ Convert string back to dict

    try:
        # ✅ Fetch only resumes belonging to the authenticated user
        result = db.session.execute(
            text(
                "SELECT id, filename, filepath, name, email, phone, skills, job_role, uploaded_at "
                "FROM resumes WHERE user_id = :user_id ORDER BY uploaded_at DESC"
            ),
            {"user_id": identity["user_id"]}
        )
        resumes = [dict(row) for row in result.mappings()]

        return jsonify({"resumes": resumes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resume_controller.route("/resume/<int:resume_id>", methods=["GET"])
def get_resume(resume_id):
    """Fetch a specific resume, ensuring only the owner can access it"""
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    token = token.split(" ")[1]  # Extract the actual token
    identity = auth_service.verify_token(token)

    if not identity:
        return jsonify({"error": "Invalid token"}), 401

    if isinstance(identity, str):
        identity = json.loads(identity)  # ✅ Convert string back to dict

    try:
        # ✅ Fetch resume details only if the user owns it
        result = db.session.execute(
            text(
                "SELECT id, filename, filepath, name, email, phone, skills, job_role, uploaded_at "
                "FROM resumes WHERE id = :resume_id AND user_id = :user_id"
            ),
            {"resume_id": resume_id, "user_id": identity["user_id"]}
        ).fetchone()

        if not result:
            return jsonify({"error": "Resume not found or unauthorized"}), 403

        return jsonify(dict(result._mapping)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@resume_controller.route("/resume/delete", methods=["POST"])
@jwt_required()  # Ensure a valid token is provided
def delete_resume():
    """
    Delete a resume based on resume_id if it belongs to the current user.
    Expects a JSON payload: { "resume_id": <id> }
    """
    data = request.get_json()
    if not data or 'resume_id' not in data:
        return jsonify({"success": False, "message": "Resume id is required."}), 400

    resume_id = data['resume_id']
    # Get current user identity; assuming it's stored as a JSON string
    current_identity = get_jwt_identity()
    try:
        user_info = json.loads(current_identity)
    except Exception:
        return jsonify({"success": False, "message": "Invalid user identity format."}), 400

    current_user_id = user_info.get("user_id")
    if not current_user_id:
        return jsonify({"success": False, "message": "User id not found in token."}), 400

    # Query the resume by id
    resume = Resume.query.filter_by(id=resume_id).first()
    if not resume:
        return jsonify({"success": False, "message": "Resume not found."}), 404

    # Ensure that the resume belongs to the current user
    if resume.user_id != current_user_id:
        return jsonify({"success": False, "message": "Unauthorized to delete this resume."}), 403

    try:
        db.session.delete(resume)
        db.session.commit()
        return jsonify({"success": True, "message": "Resume deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred while deleting the resume. " + str(e)}), 500