import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smart-price-app-secret-key-12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'smart_price.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # APScheduler Configuration
    SCHEDULER_API_ENABLED = True
    
    # Image Upload
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
