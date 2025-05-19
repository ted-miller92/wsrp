"""Server code consists of an API to access the database"""

# Import necessary libraries and modules
import re
from datetime import timedelta
from flask import Flask, request, jsonify, make_response # Flask for building the web app, request and jsonify for handling HTTP requests and responses
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database interactions
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies  # JWTManager for handling JSON Web Tokens
from flask_cors import CORS  # CORS for handling cross-origin requests
from sqlalchemy import text  # text allows execution of raw SQL queries
from flask_wtf.csrf import CSRFProtect # added for GLobal CSRF protection, add "@csrf.exempt" to CSRF insecure endpoints 
import os
from werkzeug.utils import secure_filename

# need this to load environment variables locally
from dotenv import load_dotenv
load_dotenv()

# Import necessary modules for the brute-force endpoints and hashing
from flask_limiter import Limiter  # Limiter for rate-limiting requests to prevent abuse (e.g., brute-force attacks)
from flask_limiter.util import get_remote_address  # get_remote_address to get the client IP address for rate-limiting
import bcrypt  # bcrypt for securely hashing passwords
import time  # sleep to introduce delays (e.g., for brute-force attacks or rate-limiting)
import random  # random for generating random data (e.g., for generating random strings or delays)
# Added for hashing passwords
# Ensure that when you verify passwords during login, you use bcrypt.checkpw(),
# because bcrypt hashes will always be different but can still verify the same password.


def calculate_bcrypt(password):
    """Calculate bcrypt hash of password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy()

# Initialize the Flask app
app = Flask(__name__)

# Flask JWT Configuration
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# This is so we can test locally (send token over http instead of only https)
app.config['JWT_COOKIE_SECURE'] = False

# allow JWT to be sent in cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# Set Flask secret key
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# CSRF global protection
csrf = CSRFProtect(app)

# Enable Cross-Origin Resource Sharing to allow requests from different domains
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://wsrp.space",
        "https://www.wsrp.space",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        re.compile(r"https://wsrp-git-.*-sdl101s-projects\.vercel\.app")
    ],
    "supports_credentials": True
}})

# Database configuration
# Use environment variable for SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance reasons

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Initialize Global Flask-Limiter with the app. To apply it to an enpoint, add "@limiter.limit("3 per minute") below "@app.route"
# Initialize Flask-Limiter with the app (no default limit for all routes)
limiter = Limiter(
    get_remote_address,  # Use the client's IP address for rate-limiting
    app=app
)

# Configure Limiter to send JSON response instead of default Text/HTML
# See https://flask-limiter.readthedocs.io/en/stable/recipes.html 
@app.errorhandler(429)
def ratelimit_handler(e):
    """Configure Limiter to send JSON response instead of default Text/HTML"""
    return make_response(
        jsonify(error=f"ratelimit exceeded {e.description}")
        , 429
)

failed_attempts = {}  # Dictionary to track failed login attempts per user

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
       
# Updated route for user login with combined both login routes into one. Added functionalities 
# of rate limiting, brute-force protection and bcrypt password verification
@app.route('/api/auth/login', methods=['POST'])
@csrf.exempt
@limiter.limit("3 per minute")  # Rate limiting to prevent brute-force attacks
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


# THIS IS THE SQL INJECTION VULNERABLE LOGIN ENDPOINT
@app.route('/api/sqli_vuln/auth/login', methods=['POST'])
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


# Updated for hashing and security - Define a route to create a new user
@app.route('/api/auth/register', methods=['POST'])
@csrf.exempt
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

    
# Define route to create an account (used in new account button on dashboard)
@app.route('/api/accounts/create', methods=['POST'])
@csrf.exempt
def create_account():
    """
    Creates a new account and associates it with a user if username is provided.
    VULNERABILITY: This endpoint is intentionally vulnerable as it doesn't verify user permissions.
    """
    data = request.get_json()
    account_type = data.get("account_type")
    user_name = data.get("user_name")  # Optional - if present, associates account with user
    
    # Get user_type if username is provided
    user_type = None
    if user_name:
        query = text("SELECT user_type FROM users WHERE user_name = :user_name")
        with db.engine.begin() as connection:
            result = connection.execute(query, {'user_name': user_name}).fetchone()
            if result:
                user_type = result.user_type

    # Set initial_balance based on user type
    initial_balance = float(data.get("initial_balance", 0.00))
    if user_type == "CUSTOMER":
        initial_balance = 0.00  # Force 0 for customers
    # For admin users, use the provided initial_balance

    account_number = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}" # TODO validate num doesn't exist
    
    try:
        with db.engine.begin() as connection:
            # Insert new account
            query1 = text("""
                INSERT INTO accounts (account_number, account_type, account_balance, account_interest_rate)
                VALUES (:account_number, :account_type, :initial_balance, :interest_rate)
                RETURNING account_id
            """)
            
            # Set interest rate based on account type
            interest_rate = {
                'CHECKING': 0.0005,
                'SAVINGS': 0.0015,
                'INVESTMENT': 0.0025
            }.get(account_type, 0.0)
            
            result = connection.execute(query1, {
                'account_number': account_number,
                'account_type': account_type,
                'initial_balance': initial_balance,
                'interest_rate': interest_rate
            })
            
            # Get the new account_id from the RETURNING clause
            account_id = result.fetchone().account_id
            
            # If customer (username provided), link account to user through user_accounts
            if user_name:
                query3 = text("""
                    INSERT INTO user_accounts (user_id, account_id)
                    SELECT user_id, :account_id 
                    FROM users 
                    WHERE user_name = :user_name
                """)
                connection.execute(query3, {
                    'account_id': account_id,
                    'user_name': user_name
                })

        return jsonify({
            "message": "Account created successfully",
            "status_code": 200,
            "account_id": account_id,
            "account_number": account_number
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Error creating account",
            "status_code": 500,
            "error": str(e)
        }), 500


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
            query = text("SELECT * FROM users WHERE user_name = :user_name")
            with db.engine.begin() as connection:
                result = connection.execute(query, {"user_name": user_name}).fetchone()
                if not result:
                    return jsonify({"message": "User not found", "status_code": 404}), 404
                body = {
                    "message": "User Information retrieved successfully",
                    "status_code": 200,
                    "user": result._asdict()
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
        query = text("SELECT * FROM accounts WHERE account_id = :account_id")
        with db.engine.begin() as connection:
            result = connection.execute(query, {"account_id": account_id}).fetchall()
            if not result:
                return jsonify({"message": "Account not found", "status_code": 404}), 404
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
                     WHERE user_accounts.user_id = :user_id")
        with db.engine.begin() as connection:
            result = connection.execute(query, {"user_id": user_id}).fetchall()
            if not result:
                return jsonify({"message": "No accounts found for user", "status_code": 404}), 404
            body = {
                "message": "Accounts retrieved successfully for user " + str(user_id),
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
        query = text("SELECT * FROM transactions WHERE account_id = :account_id")
        with db.engine.begin() as connection:
            result = connection.execute(query, {"account_id": account_id}).fetchall()
            if not result:
                return jsonify({"message": "No transactions found for account", "status_code": 404}), 404
            body = {
                "message": "Transactions retrieved successfully for account " + str(account_id),
                "status_code": 200,
                "transactions": [row._asdict() for row in result]
            }
            return jsonify(body), 200
    elif request.args.get('user_id'):
        user_id = request.args.get('user_id')
        query = text("SELECT * FROM transactions \
                     INNER JOIN accounts ON transactions.account_id = accounts.account_id \
                     INNER JOIN user_accounts ON accounts.account_id = user_accounts.account_id \
                     WHERE user_accounts.user_id = :user_id")
        with db.engine.begin() as connection:
            result = connection.execute(query, {"user_id": user_id}).fetchall()
            if not result:
                return jsonify({"message": "No transactions found for user", "status_code": 404}), 404
            body = {
                "message": "Transactions retrieved successfully for account " + str(user_id),
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
                     WHERE users.user_name = :user_name")
        with db.engine.begin() as connection:
            result = connection.execute(query, {"user_name": user_name}).fetchall()
            if not result:
                return jsonify({"message": "No transactions found for user", "status_code": 404}), 404
            body = {
                "message": "Transactions retrieved successfully for user " + str(user_name),
                "status_code": 200,
                "transactions": [row._asdict() for row in result]
            }
            return jsonify(body), 200
    elif request.args.get('transaction_id'):
        transaction_id = request.args.get('transaction_id')
        query = text("SELECT * FROM transactions WHERE transaction_id = :transaction_id")
        with db.engine.begin() as connection:
            result = connection.execute(query, {"transaction_id": transaction_id}).fetchall()
            if not result:
                return jsonify({"message": "Transaction not found", "status_code": 404}), 404
            body = {
                "message": "Transaction details retrieved successfully for transaction " + str(transaction_id),
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
    query = text("UPDATE accounts SET account_balance = account_balance - :amount WHERE account_id = :from_account;")
    query2 = text("UPDATE accounts SET account_balance = account_balance + :amount WHERE account_id = :to_account;")

    with db.engine.begin() as connection:
        connection.execute(query, {"amount": amount, "from_account": from_account})
        connection.execute(query2, {"amount": amount, "to_account": to_account})

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

# THIS IS THE XSS VULNERABLE LOGIN ENDPOINT
@app.route('/api/xss_vuln/auth/login', methods=['POST'])
@csrf.exempt
def login_xss_vuln():
    """
    Handles user login with XSS vulnerability.
    Note: Returns user input directly in the response without sanitization.
    """
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")

    # Query to retrieve the user by username
    query = text("SELECT * FROM users WHERE user_name = :user_name")
    with db.engine.begin() as connection:
        result = connection.execute(query, {"user_name": user_name}).fetchone()

    if not result:
        return jsonify({
            "message": "User does not exist",
            "status_code": 401,
            "user_input": user_name  # Vulnerable: returning user input directly
        }), 401

    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), result.strong_password.encode('utf-8')):
        return jsonify({
            "message": "Invalid Password",
            "status_code": 401,
            "user_input": user_name  # Vulnerable: returning user input directly
        }), 401

    # Create an access token
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

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'}), 200
    return jsonify({'message': 'Invalid file type'}), 400

@app.route('/api/vuln/upload', methods=['POST'])
def vuln_upload_file():
    print("Request.files:", request.files)
    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({'message': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("File uploaded:", filename)
    return jsonify({'message': 'File uploaded (vulnerable endpoint)'}), 200

# Run the application in debug mode (for development purposes)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)