"""Server code consists of an API to access the database"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

# SQL configuration
# This is ideally in a .env file, but for now it's here
DB_USER = 'server_user'
DB_PASSWORD = 'server_password'
DB_NAME = 'banking_db_v0'
DB_HOST = 'localhost'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/api')
def index():
    return "This is the API"


@app.route('/api/users', methods=['GET', 'POST'])
def get_users():
    # Note that there are better ways to run sql queries using SQLAlchemy,
    # but for this project we need to exhibit poor practices
    if request.method == 'GET':
        query = text("SELECT * FROM users")
        with db.engine.begin() as connection:
            result = connection.execute(query).fetchall()
            return [row._asdict() for row in result]

    elif request.method == 'POST':
        data = request.get_json()
        if data.get("user_name"):
            user_name = data.get("user_name")
            query = text("SELECT * FROM users WHERE user_name = '" + user_name + "';")
        elif data.get("user_id"):
            user_id = data.get("user_id")
            query = text("SELECT * FROM users WHERE user_id = " + user_id )

        with db.engine.begin() as connection:
            result = connection.execute(query)
            return [row._asdict() for row in result]

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")
    query1 = text("SELECT * FROM users WHERE user_name = '" + user_name + "';")
    with db.engine.begin() as connection:
        result = connection.execute(query1).fetchall()

        # Simple matching, not secure!
        if len(result) == 0:
            body = {"message": "User does not exist",
                    "status_code": 401, 
                    "result" : [row._asdict() for row in result]}
            return jsonify(body), 401

        if result[0].password != password:
            body = {
                "message": "Invalid Password", 
                "status_code": 401, 
                "result" : [row._asdict() for row in result]}
            return jsonify(body), 401

        # Return the user_id and user_type (Not a secure practice)
        body = {"user_id": result[0].user_id, "user_type": result[0].user_type}
        return jsonify(body), 200


@app.route('/api/accounts', methods=['GET'])
def get_accounts():    
    query = text("SELECT * FROM accounts")
    with db.engine.begin() as connection:
        result = connection.execute(query).fetchall()
        return [row._asdict() for row in result]

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    query = text("SELECT * FROM transactions")
    with db.engine.begin() as connection:
        result = connection.execute(query).fetchall()
        return [row._asdict() for row in result]

if __name__ == '__main__':
    app.run(debug=True)
