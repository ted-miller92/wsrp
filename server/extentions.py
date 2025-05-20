from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

# Initialize extensions without app
db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(get_remote_address)
csrf = CSRFProtect()

# Global state to track failed attempts
failed_attempts = {}

