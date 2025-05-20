from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect
from extentions import db, csrf
import random
from flask_jwt_extended import jwt_required


accounts_bp = Blueprint("accounts", __name__, url_prefix="/api/accounts")

# Define route to create an account (used in new account button on dashboard)
@accounts_bp.route('/create', methods=['POST'])
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

    # Set initial_balance to 0 if customer
    if user_type == "CUSTOMER":
        initial_balance = float(data.get("initial_balance", 0.00))
    else:
        initial_balance = 0.00

    account_number = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}" # TODO validate num doesn't exist
    
    try:
        with db.engine.begin() as connection:
            # Insert new account
            query1 = text("""
                INSERT INTO accounts (account_number, account_type, account_balance, account_interest_rate)
                VALUES (:account_number, :account_type, :initial_balance, :interest_rate)
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
            
            # Get the new account_id
            query2 = text("SELECT LAST_INSERT_ID() as account_id")
            account_id = connection.execute(query2).fetchone().account_id
            
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


# Define a route to handle user-related operations
@accounts_bp.route('/users', methods=['GET', 'POST'])
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
                result = connection.execute(query, {"user_name": user_name}).fetchall()  # Execute with parameter
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

            


@accounts_bp.route('', methods=['GET'])
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
        



# Secure money transfer with CSRF protection 
@accounts_bp.route('/transfer', methods=['POST'])
@jwt_required()
#@csrf.exempt
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