from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import create_access_token, set_access_cookies
from extentions import db, csrf

brute_bp = Blueprint("brute", __name__, url_prefix="/api/brute")


# Insecure login for brute force
@brute_bp.route('/login', methods=['POST'])
@csrf.exempt
def login_brute_force_vuln():
    """Insecure login endpoint without brute-force protection, no rate limiting, no hash checks."""
    data = request.json
    user_name = data.get('user_name')
    password = data.get('password')

    if not user_name or not password:
        return jsonify({"error": "Missing username or password"}), 400

    with db.engine.begin() as connection:
        query = text("SELECT * FROM users WHERE user_name = '" + user_name + "';")
        result = connection.execute(query).fetchall()

        # Check if the user exists
        if len(result) == 0:
            body = {"message": "User does not exist",
                    "status_code": 401, 
                    "result": [row._asdict() for row in result]}
            return jsonify(body), 401

        # Verify the password (insecure matching)
        if result[0].password_plaintext != password:
            body = {"message": "Invalid Password",
                    "status_code": 401, 
                    "result": [row._asdict() for row in result]}
            return jsonify(body), 401

        # Create an access token
        # Return user details (user_id and user_type) - also not secure
        access_token = create_access_token(identity=result[0].user_name)

        response = jsonify({
            "message": "Login successful",
            "status_code": 200,
            "user_id": result[0].user_id, 
            "user_type": result[0].user_type,
            "access_token": access_token
            })

        set_access_cookies(response, access_token)

        # Note: In other iterations, it may be better to store the JWT in a cookie to
        # protect from CSRF attacks
        return response