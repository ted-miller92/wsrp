from flask import Blueprint, request, jsonify
from sqlalchemy import text
from extentions import db

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api')

# Define a route to retrieve transaction data
@transactions_bp.route('/transactions', methods=['GET'])
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
