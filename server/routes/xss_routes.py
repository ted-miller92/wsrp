from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import create_access_token, set_access_cookies
from extentions import db, csrf
import bcrypt

xss_bp = Blueprint('xss', __name__, url_prefix='/api/xss_vuln')

@xss_bp.route('/auth/login', methods=['POST'])
@csrf.exempt
def login_xss_vuln():
    """
    Handles user login with XSS vulnerability.
    Note: Returns user input directly in the response without sanitization.
    """
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")

    query = text("SELECT * FROM users WHERE user_name = :user_name")
    with db.engine.begin() as connection:
        result = connection.execute(query, {"user_name": user_name}).fetchone()

    if not result:
        return jsonify({
            "message": "User does not exist",
            "status_code": 401,
            "user_input": user_name  # Vulnerable: returning user input directly
        }), 401

    if not bcrypt.checkpw(password.encode('utf-8'), result.strong_password.encode('utf-8')):
        return jsonify({
            "message": "Invalid Password",
            "status_code": 401,
            "user_input": user_name  # Vulnerable: returning user input directly
        }), 401

    access_token = create_access_token(identity=result.user_name)

    response = jsonify({
        "message": "Login successful",
        "status_code": 200,
        "user_id": result.user_id,
        "user_type": result.user_type,
        "access_token": access_token,
        "user_input": user_name  # Vulnerable: returning user input directly
    })

    set_access_cookies(response, access_token)
    return response
