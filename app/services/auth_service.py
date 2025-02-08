import datetime
import random
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.auth_model import User, OTPStore
from flask_jwt_extended import create_access_token, decode_token
import json

# ✅ Generate a secure OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# ✅ Store OTP in database (update if exists, insert if new)
def store_otp(email):
    otp = generate_otp()
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=90)

    existing_otp = OTPStore.query.filter_by(email=email).first()
    if existing_otp:
        existing_otp.otp = otp
        existing_otp.expires_at = expiry
    else:
        new_otp = OTPStore(email=email, otp=otp, expires_at=expiry)
        db.session.add(new_otp)

    db.session.commit()
    return otp

# ✅ Register user (OTP-based)
def register_user(email, password, name, legal_details):
    from app.tasks import send_otp_async
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"success": False, "message": "User already exists"}

    otp = store_otp(email)
    send_otp_async.delay(email, otp, name, "register")

    # ✅ Create a placeholder user entry (ensures `user_id` exists early)
    new_user = User(email=email, password_hash="", full_name=name, legal_details=legal_details)
    db.session.add(new_user)
    db.session.commit()

    return {"success": True, "message": "OTP sent. Complete registration after OTP verification."}

# ✅ Authenticate user login (OTP-based)
def authenticate_user(email, password):
    from app.tasks import send_otp_async
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {"success": False, "message": "Invalid credentials"}

    otp = store_otp(email)
    send_otp_async.delay(email, otp, user.full_name, "login")

    return {"success": True, "message": "OTP sent"}

# ✅ Validate registration OTP and create user
def validate_registration_otp(email, user_otp, password, name, legal_details):
    from app.tasks import send_otp_async
    otp_entry = OTPStore.query.filter_by(email=email).first()

    if not otp_entry:
        return {"success": False, "message": "No OTP found. Please request a new one."}

    if datetime.datetime.utcnow() > otp_entry.expires_at:
        return {"success": False, "message": "OTP expired. Request a new one."}

    if otp_entry.otp != user_otp:
        return {"success": False, "message": "Invalid OTP. Please try again."}

    # ✅ Insert user after OTP validation
    hashed_password = generate_password_hash(password)
    user = User.query.filter_by(email=email).first()
    
    if user and user.password_hash == "":  # ✅ Update placeholder user
        user.password_hash = hashed_password
        user.legal_details = legal_details
    else:
        user = User(email=email, password_hash=hashed_password, full_name=name, legal_details=legal_details)
        db.session.add(user)

    db.session.commit()

    db.session.delete(otp_entry)
    db.session.commit()

    send_otp_async.delay(email, None, name, "registration_complete")

    return {"success": True, "message": "User registered successfully"}

# ✅ Validate login OTP and generate access token
def validate_login_otp(email, user_otp):
    otp_entry = OTPStore.query.filter_by(email=email).first()

    if not otp_entry:
        return {"success": False, "message": "No OTP found. Please request a new one."}

    if datetime.datetime.utcnow() > otp_entry.expires_at:
        return {"success": False, "message": "OTP expired. Request a new one."}

    if otp_entry.otp != user_otp:
        return {"success": False, "message": "Invalid OTP. Please try again."}

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"success": False, "message": "User not found. Please register first."}

    access_token = create_access_token(identity=json.dumps({"user_id": user.user_id, "email": user.email}))

    return {
        "success": True,
        "message": "OTP validated successfully",
        "token": access_token
    }


# ✅ Reset password request (OTP-based)
def reset_password_request_service(email):
    from app.tasks import send_otp_async
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"success": False, "message": "Email not found"}

    otp = store_otp(email)
    send_otp_async.delay(email, otp, user.full_name, "password_reset")

    return {"success": True, "message": "Password reset OTP sent"}

# ✅ Update password after OTP verification
def update_password_service(email, user_otp, new_password):
    otp_entry = OTPStore.query.filter_by(email=email).first()

    if not otp_entry or otp_entry.otp != user_otp:
        return {"success": False, "message": "Invalid OTP"}

    if datetime.datetime.utcnow() > otp_entry.expires_at:
        return {"success": False, "message": "OTP expired"}

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"success": False, "message": "User not found"}

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    db.session.delete(otp_entry)
    db.session.commit()

    return {"success": True, "message": "Password updated successfully"}
    
def verify_token(token):
    try:
        decoded_token = decode_token(token)
        
        # ✅ Convert 'sub' from string back to dict
        identity = decoded_token["sub"]
        if isinstance(identity, str):
            identity = json.loads(identity)

        if not isinstance(identity, dict):
            print(f"❌ ERROR: 'sub' is not a dict after conversion -> {identity}")
            return None

        return identity  # ✅ Return correct user data
    except Exception as e:
        print(f"❌ JWT Decode Error -> {e}")
        return None

