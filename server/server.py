"""Server code consists of an API to access the database"""

# Import necessary libraries and modules
import re
from datetime import timedelta
from flask import Flask, request, jsonify, make_response # Flask for building the web app, request and jsonify for handling HTTP requests and responses
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required
from extentions import db, limiter, csrf, jwt
# from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database interactions
#from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies  # JWTManager for handling JSON Web Tokens
from flask_cors import CORS  # CORS for handling cross-origin requests
from sqlalchemy import text  # text allows execution of raw SQL queries
from routes import register_blueprints # Imports blueprint routes
from routes.csrf_routes import csrf_bp
csrf.exempt(csrf_bp)
from dotenv import load_dotenv
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

# Update CORS line to this once testing is done and ready to psuh - CORS(app, resources={
#     r"/api/*": {
#         "origins": ["https://wsrp.space/", "https://www.wsrp.space/"],
#         "supports_credentials": True
#     }
# })
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`


load_dotenv()


# Initialize the Flask app
app = Flask(__name__)

# Load JWT secret key from .env
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# This is so we can test locally (send token over http instead of only https)
app.config['JWT_COOKIE_SECURE'] = False
# allow JWT to be sent in cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]


# Database configuration
# Note: It's a security best practice to store these in a .env file and not hard-code credentials 
# - Updated and moved 
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')




# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance reasons

# CSRF global protection 
#csrf = CSRFProtect(app)

# Enable Cross-Origin Resource Sharing to allow requests from different domains
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "supports_credentials": True
    }
})



jwt.init_app(app)
db.init_app(app)
csrf.init_app(app)
limiter.init_app(app)

register_blueprints(app) # Registers blueprints for routes files

from routes.auth_routes import auth_bp
csrf.exempt(auth_bp)



# Configure Limiter to send JSON response instead of default Text/HTML
# See https://flask-limiter.readthedocs.io/en/stable/recipes.html 
@app.errorhandler(429)
def ratelimit_handler(e):
    """Configure Limiter to send JSON response instead of default Text/HTML"""
    return make_response(
        jsonify(error=f"ratelimit exceeded {e.description}")
        , 429
)


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
       



# Run the application in debug mode (for development purposes)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)