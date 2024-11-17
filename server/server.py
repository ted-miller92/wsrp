"""Server code consists of an API to access the database"""

# Import necessary libraries and modules
from flask import Flask, request, jsonify  # Flask for building the web app, request and jsonify for handling HTTP requests and responses
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database interactions
from flask_cors import CORS  # CORS for handling cross-origin requests
from sqlalchemy import text  # text allows execution of raw SQL queries

# Initialize the Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing to allow requests from different domains
CORS(app)

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

# Define a basic route to confirm the API is running
@app.route('/api')
def index():
    return "This is the API"

# Define a route to handle user-related operations
@app.route('/api/users', methods=['GET', 'POST'])
def get_users():
    """
    Handles retrieving all users (GET) or querying for a specific user (POST).
    Note: Deliberately uses insecure practices for educational purposes.
    """
    if request.method == 'GET':
        # Query to retrieve all users from the 'users' table
        query = text("SELECT * FROM users")
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()  # Fetch all rows from the query result
            return [row._asdict() for row in result]  # Return results as a list of dictionaries

    elif request.method == 'POST':
        # Parse JSON data from the request body
        data = request.get_json()
        
        # Determine whether to query by user_name or user_id
        if data.get("user_name"):
            user_name = data.get("user_name")
            query = text("SELECT * FROM users WHERE user_name = '" + user_name + "';")
        elif data.get("user_id"):
            user_id = data.get("user_id")
            query = text("SELECT * FROM users WHERE user_id = " + user_id)

        with db.engine.begin() as connection:
            result = connection.execute(query)  # Execute the query
            return [row._asdict() for row in result]  # Return results as a list of dictionaries

# Define a route for user login
@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Handles user login by validating credentials.
    Note: Uses insecure practices such as plain-text password storage and SQL injection vulnerability.
    """
    # Parse JSON data from the request body
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")

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

        # Return user details (user_id and user_type) - also not secure
        body = {"user_id": result[0].user_id, "user_type": result[0].user_type}
        return jsonify(body), 200

# Define a route to retrieve account data
@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """
    Retrieves all accounts from the 'accounts' table.
    """
    query = text("SELECT * FROM accounts")  # SQL query to fetch all accounts
    with db.engine.begin() as connection:
        result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
        return [row._asdict() for row in result]  # Return results as a list of dictionaries

# Define a route to retrieve transaction data
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """
    Retrieves all transactions from the 'transactions' table.
    """
    query = text("SELECT * FROM transactions")  # SQL query to fetch all transactions
    with db.engine.begin() as connection:
        result = connection.execute(query).fetchall()  # Execute the query and fetch all rows
        return [row._asdict() for row in result]  # Return results as a list of dictionaries

# Run the application in debug mode (for development purposes)
if __name__ == '__main__':
    app.run(debug=True)
