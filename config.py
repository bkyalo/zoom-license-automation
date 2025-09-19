import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Zoom API Credentials
    ZOOM_ACCOUNT_ID = os.getenv('ZOOM_ACCOUNT_ID')
    ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID')
    ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET')
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    
    # Default user email for testing
    DEFAULT_USER_EMAIL = os.getenv('DEFAULT_USER_EMAIL')
    
    # Users who should never be unassigned
    EXEMPT_USERS = [email.strip() for email in os.getenv('EXEMPT_USERS', '').split(',') if email.strip()]
    
    # API Endpoints
    ZOOM_AUTH_URL = "https://zoom.us/oauth/token"
    ZOOM_API_BASE_URL = "https://api.zoom.us/v2"
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration values are set."""
        required_vars = [
            'ZOOM_ACCOUNT_ID',
            'ZOOM_CLIENT_ID',
            'ZOOM_CLIENT_SECRET',
            'DEFAULT_USER_EMAIL',
            'DB_HOST',
            'DB_USER',
            'DB_PASSWORD',
            'DB_NAME',
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID',
            'EXEMPT_USERS'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required configuration: {', '.join(missing_vars)}")

# Validate configuration when imported
Config.validate_config()
