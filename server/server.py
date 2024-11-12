from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json

app = Flask(__name__)

# SQL configuration
# This is ideally in a .env file, but for now it's here
db_user = 'server_user'
db_password = 'server_password'
db_name = 'banking_db_v0'
db_host = 'localhost'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'.format(db_user=db_user, db_password=db_password, db_host=db_host, db_name=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/api')
def index():
    return "This is the API"


@app.route('/api/users', methods=['GET', 'POST'])
def get_users():
    # Note that there are better ways to run sql queries using SQLAlchemy, but for this project we need to exhibit poor practices
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
            query = text("SELECT * FROM users WHERE user_id = "+ user_id )
        
        with db.engine.begin() as connection:
            result = connection.execute(query)
            return [row._asdict() for row in result]
    

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

