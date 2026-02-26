import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-in-production'
    
    # MongoDB settings
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/cryptoscore_pro'
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CoinGecko API
    COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
    
    # Currency conversion
    USD_TO_INR = 83.12
    
    # Prediction settings
    PREDICTION_DAYS = [1, 7, 30]  # Days to predict ahead
    
    # Rate limiting
    MAX_PREDICTIONS_PER_DAY = 50


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/cryptoscore_pro_test'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}