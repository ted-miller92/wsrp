from flask import Blueprint

# Import all blueprints from other route files
from .auth_routes import auth_bp
from .sqli_routes import sqli_bp
from .csrf_routes import csrf_bp
from .xss_routes import xss_bp
from .brute_routes import brute_bp
from .accounts_routes import accounts_bp
from .transactions_routes import transactions_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(sqli_bp)
    app.register_blueprint(csrf_bp)
    app.register_blueprint(xss_bp)
    app.register_blueprint(brute_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(transactions_bp)
