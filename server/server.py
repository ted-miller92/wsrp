"""Server code consists of an API to access the database"""

# Import necessary libraries and modules
from datetime import timedelta
from flask import Flask, request, jsonify  # Flask for building the web app, request and jsonify for handling HTTP requests and responses
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database interactions
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies  # JWTManager for handling JSON Web Tokens
from flask_cors import CORS  # CORS for handling cross-origin requests
from sqlalchemy import text  # text allows execution of raw SQL queries
from flask_wtf.csrf import CSRFProtect # added for GLobal CSRF protection, add "@csrf.exempt" to CSRF insecure endpoints 

# Import necessary modules for the brute-force endpoints
from flask_limiter import Limiter  # Limiter for rate-limiting requests to prevent abuse (e.g., brute-force attacks)
from flask_limiter.util import get_remote_address  # get_remote_address to get the client IP address for rate-limiting
import bcrypt  # bcrypt for securely hashing passwords
from time import sleep  # sleep to introduce delays (e.g., for brute-force attacks or rate-limiting)
import random  # random for generating random data (e.g., for generating random strings or delays)
import mysql.connector
import bcrypt

# Initialize the Flask app
app = Flask(__name__)
jwt = JWTManager(app)
# Flask JWT Configuration
app.config['JWT_SECRET_KEY'] = 'secret_key' # change this and save in .env file

# This is so we can test locally (send token over http instead of only https)
app.config['JWT_COOKIE_SECURE'] = False

# allow JWT to be sent in cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# CSRF global protection 
csrf = CSRFProtect(app)

# Enable Cross-Origin Resource Sharing to allow requests from different domains
CORS(app, resources={r"/api/*": {"origin": "http://localhost:5173", "supports_credentials": True}})

# Database configuration
# Note: It's a security best practice to store these in a .env file and not hard-code credentials
DB_USER = 'server_user'  # Database username
DB_PASSWORD = 'server_password'  # Database password
DB_NAME = 'banking_db_v0'  # Name of the database
DB_HOST = 'localhost'  # Host address for the database

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance reasons

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Added root route 1-18
@app.route('/')
def home():
    """Returns a confirmation that the server is running"""
    return "Welcome to the Flask API!"

# Define a basic route to confirm the API is running
@app.route('/api')
def index():
    """Returns a confirmation that the API is running"""
    return "API is up and running"

# Initialize Global Flask-Limiter with the app. To apply it to an enpoint, add "@limiter.limit("3 per minute") below "@app.route"
# Initialize Flask-Limiter with the app (no default limit for all routes)
limiter = Limiter(
    get_remote_address,  # Use the client's IP address for rate-limiting
    app=app
)

# Secure login with brute-force protection. Rate-Limiting, tracking failed attempts per IP implemented
failed_attempts = {}  # Dictionary to track failed login attempts per user
       
# Define a route for user login
# We will treat this endpoint as insecure and CSRF vulnerable for now, as @csrf.exempt has been added
@app.route('/api/auth/login', methods=['POST'])
@csrf.exempt  # Flask-WTF automatically applies CSRF protection to forms unless exempted
@limiter.limit("3 per minute")  # Apply rate limiting using the decorator
def login():
    """
    Handles user login by validating credentials.
    Note: Uses insecure practices such as plain-text password storage and SQL 
    injection vulnerability.
    """
    # Parse JSON data from the request body
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")

    # strip any unallowed characters
    user_name = user_name.strip("';#$%&*()_+=@/\\|~`")
    password = password.strip("';#$%&*()_+=@/\\|~`")

    # Query to retrieve the user by username
    query1 = text("SELECT * FROM users WHERE user_name = '" + user_name + "';")
    with db.engine.begin() as connection:
        result = connection.execute(query1).fetchall()  # Fetch all matching rows

        # Check if the user exists
        if len(result) == 0:
            body = {"message": "User does not exist",
                    "status_code": 401, 
                    "result": [row._asdict() for row in result]}
            return jsonify(body), 401

        # Check if the user has exceeded failed attempts
        if user_name in failed_attempts and failed_attempts[user_name] >= 3:
            sleep(5)  # Introduce artificial delay
            return jsonify({"error": "Too many failed attempts. Try again later."}), 403

        # Verify the password (insecure matching)
        if result[0].password != password:
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

# THIS IS THE SQL INJECTION VULNERABLE LOGIN ENDPOINT
# we will treat this endpoint as insecure and CSRF vulnerable for now, as @csrf.exempt has been added 
@app.route('/api/sqli_vuln/auth/login', methods=['POST'])
@csrf.exempt  # Flask-WTF automatically applies CSRF protection to forms unless exempted
def login_sqli_vuln():
    """
    Handles user login by validating credentials.
    Note: Uses insecure practices such as plain-text password storage and SQL 
    injection vulnerability.
    """
    # Parse JSON data from the request body
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")

    # This is where we WOULD strip any unallowed characters

    # Query to retrieve the user by username
    query1 = text("SELECT * FROM users WHERE user_name = '" + user_name + "';")
    with db.engine.begin() as connection:
        result = connection.execute(query1).fetchall()  # Fetch all matching rows

        # Check if the user exists
        if len(result) == 0:
            body = {"message": "User does not exist",
                    "status_code": 401, 
                    "result": [row._asdict() for row in result]}
            return jsonify(body), 401

        # Verify the password (insecure matching)
        if result[0].password != password:
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

# Define a route to create a new user
@app.route('/api/auth/register', methods=['POST'])
@csrf.exempt
def register():
    """
    Handles user registration.
    Note: Uses insecure practices such as plain-text password storage and SQL 
    injection vulnerability.
    """
    # Parse JSON data from the request body
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    user_type = data.get("user_type")

    # strip any unallowed characters
    user_name = user_name.strip("';#$%&*()_+=@/\\|~`")
    password = password.strip("';#$%&*()_+=@/\\|~`")
    first_name = first_name.strip("';#$%&*()_+=@/\\|~`")
    last_name = last_name.strip("';#$%&*()_+=@/\\|~`")
    email = email.strip("';#$%&*()_+=@/\\|~`")

    query_1 = text("SELECT * FROM users WHERE user_name = '" + user_name + "';")
    with db.engine.begin() as connection:
        result = connection.execute(query_1).fetchall()  # Fetch all matching rows

        # Check if the user already exists
        if len(result) > 0:
            body = {"message": "User already exists",
                    "status_code": 401, 
                    "result": [row._asdict() for row in result]}
            return jsonify(body), 401

        # Check if the email already exists
        query_2 = text("SELECT * FROM users WHERE email = '" + email + "';")
        result = connection.execute(query_2).fetchall()  # Fetch all matching rows
        if len(result) > 0:
            body = {"message": "Email already exists",
                    "status_code": 401, 
                    "result": [row._asdict() for row in result]}
            return jsonify(body), 401

        # Insert the new user into the 'users' table
        query_3 = text("INSERT INTO users \
                       (user_name, password, first_name, last_name, email, user_type) \
                       VALUES \
                       ('" + user_name + "', '" + password + "', '" + first_name + "', '" + last_name + "', '" + email + "', '" + user_type + "');")
        connection.execute(query_3)  # Execute the query
        body = {
            "message": "User created successfully",
            "status_code": 200
        }
        return jsonify(body), 200

@app.route('/api/auth/logout', methods=['POST'])
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

# Define a route to handle user-related operations
@app.route('/api/users', methods=['GET', 'POST'])
def get_users():
    """
    Handles retrieving all users (GET) or querying for a specific user (POST).
    Note: This route is more secure from SQL injection attacks than the route 
    defined in the "sql_injection_vulnerable" branch
    """
    if request.method == 'GET':
        if request.args.get('user_name'):
            user_name = request.args.get('user_name')
            query = text("SELECT * FROM users WHERE user_name = " + user_name)
            with db.engine.begin() as connection:
                result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
                body = {
                    "message": "User Information retrieved successfully",
                    "status_code": 200,
                    "user": result[0]._asdict()
                }
                return jsonify(body), 200
        else:
            # Query to retrieve all users from the 'users' table
            query = text("SELECT * FROM users")
            with db.engine.begin() as connection:
                result = connection.execute(query).fetchall()  # Fetch all rows from the query result
                return [row._asdict() for row in result]  # Return results as a list of dictionaries

@app.route('/api/accounts', methods=['GET'])
# @jwt_required() # uncomment this line if you want to use JWT token authentication
def get_account():
    """
    Retrieves an account from the 'accounts' table based on the provided account_id.
    """
    if request.args.get('account_id'):
        account_id = request.args.get('account_id')
        query = text("SELECT * FROM accounts WHERE account_id = " + account_id)
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "Account retrieved successfully",
                "status_code": 200,
                "acount": result[0]._asdict()
            }
            return jsonify(body), 200

    elif request.args.get('user_id'):
        user_id = request.args.get('user_id')
        query = text("SELECT * FROM accounts \
                     INNER JOIN user_accounts ON accounts.account_id = user_accounts.account_id \
                     WHERE user_accounts.user_id = " + user_id)
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "Accounts retrieved successfully for user " + user_id,
                "status_code": 200,
                "accounts": [row._asdict() for row in result]
            }
            return jsonify(body), 200
    else:
        # returns all accounts
        query = text("SELECT * FROM accounts")
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "Accounts retrieved successfully",
                "status_code": 200,
                "accounts": [row._asdict() for row in result]
            }
            return jsonify(body), 200

# Define a route to retrieve transaction data
@app.route('/api/transactions', methods=['GET'])
# @jwt_required() # uncomment this if you want to use JWT token authentication
def get_transactions():
    """
    Retrieves transactions from the 'transactions' table.
    """
    if request.args.get('account_id'):
        account_id = request.args.get('account_id')
        query = text("SELECT * FROM transactions WHERE account_id = " + account_id)
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "Transactions retrieved successfully for account " + account_id,
                "status_code": 200,
                "transactions": [row._asdict() for row in result]
            }
            return jsonify(body), 200
    elif request.args.get('user_id'):
        user_id = request.args.get('user_id')
        query = text("SELECT * FROM transactions \
                     INNER JOIN accounts ON transactions.account_id = accounts.account_id \
                     INNER JOIN user_accounts ON accounts.account_id = user_accounts.account_id \
                     WHERE user_accounts.user_id = " + user_id)
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "Transactions retrieved successfully for account " + user_id,
                "status_code": 200,
                "transactions": [row._asdict() for row in result]
            }
            return jsonify(body), 200
    elif request.args.get('user_name'):
        user_name = request.args.get('user_name')
        query = text("SELECT * FROM transactions \
                     INNER JOIN accounts ON transactions.account_id = accounts.account_id \
                     INNER JOIN user_accounts ON accounts.account_id = user_accounts.account_id \
                     INNER JOIN users ON user_accounts.user_id = users.user_id \
                     WHERE users.user_name = " + user_name)
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "Transactions retrieved successfully for user " + user_name,
                "status_code": 200,
                "transactions": [row._asdict() for row in result]
            }
            return jsonify(body), 200
    elif request.args.get('transaction_id'):
        transaction_id = request.args.get('transaction_id')
        query = text("SELECT * FROM transactions WHERE transaction_id = " + transaction_id)
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "Transaction details retrieved successfully for transaction " + transaction_id,
                "status_code": 200,
                "transactions": [row._asdict() for row in result]
            }
            return jsonify(body), 200
    else:
        query = text("SELECT * FROM transactions")  # SQL query to fetch all transactions
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
            body = {
                "message": "All transactions retrieved successfully",
                "status_code": 200,
                "transactions": [row._asdict() for row in result]
            }
            return jsonify(body), 200

# Insecure money transfer 
@app.route('/api/csrf_vuln/transfer', methods=['POST'])
@csrf.exempt  # Flask-WTF automatically applies CSRF protection to forms unless exempted
def transfer_money():
    """
    Simulates a CSRF-vulnerable money transfer.
    This endpoint allows unauthorized transactions from external sites.
    """
    data = request.get_json()
    from_account = data.get("from_account")
    to_account = data.get("to_account")
    amount = data.get("amount")

    # Directly execute SQL query (no authentication check)
    query = text(f"UPDATE accounts SET account_balance = account_balance - {amount} WHERE account_id = {from_account};")
    query2 = text(f"UPDATE accounts SET account_balance = account_balance + {amount} WHERE account_id = {to_account};")

    with db.engine.begin() as connection:
        connection.execute(query)
        connection.execute(query2)

    return jsonify({"message": "Transfer successful", "status_code": 200})

# Secure money transfer with CSRF protection 
@app.route('/api/transfer', methods=['POST'])
@jwt_required()
def secure_transfer():
    """
    Secure version of the money transfer API using CSRF tokens and JWT authentication.
    """
    data = request.get_json()
    from_account = data.get("from_account")
    to_account = data.get("to_account")
    amount = data.get("amount")

    if not from_account or not to_account or not amount:
        return jsonify({"message": "Invalid data", "status_code": 400}), 400

    query = text("UPDATE accounts SET account_balance = account_balance - :amount WHERE account_id = :from_account")
    query2 = text("UPDATE accounts SET account_balance = account_balance + :amount WHERE account_id = :to_account")

    with db.engine.begin() as connection:
        connection.execute(query, {"amount": amount, "from_account": from_account})
        connection.execute(query2, {"amount": amount, "to_account": to_account})

    return jsonify({"message": "Secure transfer successful", "status_code": 200})

# 2 New API Endpoints for Brute-force below 

# suggest deleting this function as we already have a way to create a db connection
# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="server_user",
        password="server_password",
        database="banking_db_v0"
    )

# Insecure login for brute force
@app.route('/api/brute_force_vuln/login', methods=['POST'])
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
        if result[0].password != password:
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

@app.route("/secure_login", methods=["POST"])
@csrf.exempt
@limiter.limit("3 per minute")  # Apply rate limiting using the decorator
def secure_login():
    """Secure login endpoint with brute-force protection."""
    # global failed_attempts
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Fetch the stored password hash from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE user_name = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Check if the user has exceeded failed attempts
    if username in failed_attempts and failed_attempts[username] >= 3:
        sleep(5)  # Introduce artificial delay
        return jsonify({"error": "Too many failed attempts. Try again later."}), 403

    if bcrypt.checkpw(password.encode("utf-8"), user['password'].encode('utf-8')):
        failed_attempts[username] = 0  # Reset failed attempts on success
        return jsonify({"message": "Login successful!"}), 200
    else:
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        sleep(random.uniform(1, 3))  # Introduce random delay to prevent timing attacks
        return jsonify({"error": "Invalid credentials"}), 401

# Reset failed attempts route
@app.route("/api/auth/reset_failed_attempts", methods=["POST"])
@csrf.exempt
def reset_failed_attempts():
    """Reset the failed login attempts for a specific user."""
    # global failed_attempts
    data = request.get_json()
    user_name = data.get("user_name")

    if user_name in failed_attempts:
        del failed_attempts[user_name]

    return jsonify({"message": f"Failed attempts for {user_name} have been reset."}), 200

# Run the application in debug mode (for development purposes)
if __name__ == '__main__':
    app.run(debug=True)
