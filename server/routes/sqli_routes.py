from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import create_access_token, set_access_cookies
from extentions import db, csrf

sqli_bp = Blueprint('sqli', __name__, url_prefix='/api/sqli')

# THIS IS THE SQL INJECTION VULNERABLE LOGIN ENDPOINT
@sqli_bp.route('/auth/login', methods=['POST'])
@csrf.exempt  # CSRF protection is intentionally disabled for vulnerability
def login_sqli_vuln():
    """
    Insecure SQL Injection vulnerable login endpoint.
    - Uses plain-text password matching.
    - Directly concatenates user input into the SQL query (SQL Injection risk).
    """
    # Parse JSON data from request body
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")

    if not user_name or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # INSECURE QUERY (INTENTIONALLY VULNERABLE TO SQL INJECTION)
    query1 = text(f"SELECT * FROM users WHERE user_name = '{user_name}';")
    
    with db.engine.begin() as connection:
        result = connection.execute(query1).fetchall()  # Fetch all matching rows

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

        # **Create an access token (Still insecure)**
        access_token = create_access_token(identity=result[0].user_name)

        response = jsonify({
            "message": "Login successful (but vulnerable to SQL injection!)",
            "status_code": 200,
            "user_id": result[0].user_id, 
            "user_type": result[0].user_type,
            "access_token": access_token
        })

        set_access_cookies(response, access_token)

        return response
