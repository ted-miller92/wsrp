from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required
from flask_wtf.csrf import CSRFProtect
# from server import csrf  # this gets the global csrf instance from your app

from sqlalchemy import text
import re
import time
import random
import bcrypt
#from server import db, limiter, failed_attempts
from extentions import db, limiter
from extentions import failed_attempts



auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")



# Updated route for user login with combined both login routes into one. Added functionalities 
# of rate limiting, brute-force protection and bcrypt password verification
@auth_bp.route('/login', methods=['POST'])
# @csrf_exempt --removed to use exempt at bottom instead
@limiter.limit("3 per minute")
def login():
    """Handles user login securely with brute-force protection and JWT authentication."""
    data = request.get_json()
    user_name = data.get("user_name")  # Standardizing the name from "username"
    password = data.get("password")

    if not user_name or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # strip any unallowed characters
    user_name = re.sub(r"[';#$%&*()_+=@/\\|~]", "", user_name)

    # Secure query using parameterized SQL (prevents SQL injection)
    query = text("SELECT user_id, user_name, user_type, strong_password FROM users WHERE user_name = :user_name")
    
    with db.engine.begin() as connection:
        result = connection.execute(query, {"user_name": user_name}).fetchone()

    if not result:
        print(f"DEBUG: User {user_name} does not exist!")
        return jsonify({"message": "User does not exist", "status_code": 401}), 401

    strong_password_hash = result.strong_password  # bcrypt hash stored in DB

    # **Print Debugging Info**
    print(f"DEBUG: Stored bcrypt hash from DB: {strong_password_hash}")
    print(f"DEBUG: Entered password: {password}")

    # **Brute-force protection**
    if user_name in failed_attempts and failed_attempts[user_name] >= 3:
        time.sleep(5)  # Introduce artificial delay to slow down attackers
        return jsonify({"error": "Too many failed attempts. Try again later."}), 403

    # **Password Verification**
    if bcrypt.checkpw(password.encode('utf-8'), strong_password_hash.encode('utf-8')):
        print("DEBUG: Bcrypt password match!")

        # Reset failed attempts on successful login
        failed_attempts[user_name] = 0

        # Generate JWT access token
        access_token = create_access_token(identity=result.user_name)

        response = jsonify({
            "message": "Login successful",
            "status_code": 200,
            "user_id": result.user_id,
            "user_type": result.user_type,
            "access_token": access_token,
            "security_level": "strong"
        })

        set_access_cookies(response, access_token)  # Set authentication cookies
        return response

    else:
        print("DEBUG: Bcrypt password does NOT match!")

        # Increment failed login attempts and introduce random delay
        failed_attempts[user_name] = failed_attempts.get(user_name, 0) + 1
        time.sleep(random.uniform(1, 3))  # Random delay to prevent timing attacks

        return jsonify({"message": "Invalid Password", "status_code": 401}), 401
    



# Updated for hashing and security - Define a route to create a new user
@auth_bp.route('/register', methods=['POST'])
# @csrf_exempt --removed to use exempt at bottom instead
def register():
    """
    Handles user registration securely.
    Checks separately if the username and email already exist before inserting a new user.
    Stores the plaintext password (for demonstration) and its bcrypt-hashed version.
    """
    # Parse JSON data from request
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    user_type = data.get("user_type")

    if not user_name or not password or not first_name or not last_name or not email or not user_type:
        return jsonify({"message": "Missing required fields", "status_code": 400}), 400

    # Strip special characters from non-password fields
    user_name = re.sub(r"[;'#$%&*()_+=@/\\|~`]", "", user_name)
    first_name = re.sub(r"[;'#$%&*()_+=@/\\|~`]", "", first_name)
    last_name = re.sub(r"[;'#$%&*()_+=@/\\|~`]", "", last_name)
    email = re.sub(r"[;'#$%&*()_+=@/\\|~`]", "", email)

    # Don't strip the password! Some special characters are valid in passwords.

    # **Check if the username already exists**
    query_check_user = text("SELECT user_id FROM users WHERE user_name = :user_name")
    with db.engine.begin() as connection:
        existing_user = connection.execute(query_check_user, {"user_name": user_name}).fetchone()
        if existing_user:
            return jsonify({"message": "Username already taken", "status_code": 409}), 409

    # **Check if the email already exists**
    query_check_email = text("SELECT user_id FROM users WHERE email = :email")
    with db.engine.begin() as connection:
        existing_email = connection.execute(query_check_email, {"email": email}).fetchone()
        if existing_email:
            return jsonify({"message": "Email already registered", "status_code": 409}), 409

    # **Hash the password securely using bcrypt**
    bcrypt_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # **Insert user into database with plaintext and hashed password**
    query_insert = text("""
        INSERT INTO users (user_name, first_name, last_name, email, user_type, password_plaintext, strong_password)
        VALUES (:user_name, :first_name, :last_name, :email, :user_type, :password_plaintext, :strong_password)
    """)
    with db.engine.begin() as connection:
        connection.execute(query_insert, {
            "user_name": user_name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "user_type": user_type,
            "password_plaintext": password,  # Storing plaintext password for demonstration
            "strong_password": bcrypt_hash   # Storing bcrypt-hashed password for security
        })

    return jsonify({"message": "User registered successfully", "status_code": 201}), 201

# Logout route
@auth_bp.route('/logout', methods=['POST'])
@jwt_required() 
def logout():
    """Destroys/nullifies the jwt token
    This endpoint is only used with the version of the server that uses cookies for
    JWT token authentication/storage
    """
    response = jsonify({
        "message": "Logout successful",
        "status_code": 200
        })
    unset_jwt_cookies(response)
    return response


# Reset failed attempts route
@auth_bp.route("/reset_failed_attempts", methods=["POST"])
# @csrf_exempt --removed to use exempt at bottom instead
def reset_failed_attempts():
    """Reset the failed login attempts for a specific user."""
    # global failed_attempts
    data = request.get_json()
    user_name = data.get("user_name")

    if user_name in failed_attempts:
        del failed_attempts[user_name]

    return jsonify({"message": f"Failed attempts for {user_name} have been reset."}), 200


# CSRF exemptions for insecure routes
from extentions import csrf

csrf.exempt(login)
csrf.exempt(register)
csrf.exempt(reset_failed_attempts)