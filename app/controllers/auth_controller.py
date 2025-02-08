from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, authenticate_user, validate_registration_otp, validate_login_otp,reset_password_request_service,update_password_service
from app.models.auth_model import User 
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from flask import request

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    result = register_user(data["email"], data["password"], data["name"], data["legal_details"])
    return jsonify(result), 201 if result["success"] else 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    result = authenticate_user(data["email"], data["password"])
    return jsonify(result), 200 if result["success"] else 401

@auth_bp.route("/validate-registration-otp", methods=["POST"])
def validate_registration_otp_api():
    data = request.json
    result = validate_registration_otp(data["email"], data["otp"], data["password"], data["name"], data["legal_details"])
    return jsonify(result), 200 if result["success"] else 400

@auth_bp.route("/validate-login-otp", methods=["POST"])
def validate_login_otp_api():
    data = request.json
    result = validate_login_otp(data["email"], data["otp"])
    return jsonify(result), 200 if result["success"] else 400

@auth_bp.route("/user", methods=["GET"])
def get_user():
    email = request.args.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400

    # ✅ Check if any users exist in the table
    if User.query.count() == 0:
        return jsonify({"success": False, "message": "No users found in the database"}), 200

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    return jsonify({
        "success": True,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password_request():
    data = request.json
    result = reset_password_request_service(data["email"])
    return jsonify(result), 200 if result["success"] else 400

@auth_bp.route("/update-password", methods=["POST"])
def update_password():
    data = request.json
    result = update_password_service(data["email"], data["otp"], data["new_password"])
    return jsonify(result), 200 if result["success"] else 400

import json

@auth_bp.route("/user-details", methods=["GET"])
@jwt_required()
def get_user_details():
    identity = get_jwt_identity()

    # ✅ Convert JSON string back to dict
    if isinstance(identity, str):
        try:
            identity = json.loads(identity)
        except json.JSONDecodeError:
            return jsonify({"success": False, "message": "Invalid token format"}), 422

    if not isinstance(identity, dict) or "email" not in identity:
        return jsonify({"success": False, "message": "Invalid token structure"}), 422

    user = User.query.filter_by(email=identity["email"]).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    return jsonify({
        "success": True,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 200

@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)  # This decorator ensures the endpoint is accessed with a valid refresh token
def refresh_token():
    """
    Refresh the access token and optionally issue a new refresh token.
    Expects the client to send a valid refresh token (typically via headers or cookies).
    """
    # Extract the identity from the valid refresh token.
    current_identity = get_jwt_identity()
    
    # Create a new access token.
    new_access_token = create_access_token(
        identity=current_identity
    )
    
    return jsonify({
        "accessToken": new_access_token
    }), 200