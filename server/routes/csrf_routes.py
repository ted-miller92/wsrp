from flask import Blueprint, request, jsonify
from sqlalchemy import text
from extentions import db, csrf

csrf_bp = Blueprint('csrf', __name__, url_prefix='/api/csrf_vuln')

@csrf_bp.route('/transfer', methods=['POST'])
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

    query = text(f"UPDATE accounts SET account_balance = account_balance - {amount} WHERE account_id = {from_account};")
    query2 = text(f"UPDATE accounts SET account_balance = account_balance + {amount} WHERE account_id = {to_account};")

    with db.engine.begin() as connection:
        connection.execute(query)
        connection.execute(query2)

    return jsonify({"message": "Transfer successful", "status_code": 200})
