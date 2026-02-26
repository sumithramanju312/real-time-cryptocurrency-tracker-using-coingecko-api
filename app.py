import os
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

from config import config
from models import init_db, mongo
from models.user import User

# Import blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.prediction import prediction_bp
from routes.api import api_bp


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    CSRFProtect(app)
    init_db(app)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(api_bp)
    
    # Context processors
    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'CryptoScore Pro',
            'current_year': 2025
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app


# Create application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)