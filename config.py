import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost:5432/medical_device_management')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    
    # Email settings
    # Default is Gmail SMTP, but can be changed to SendGrid through API key
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@medicaldevices.com')
    
    # SendGrid settings (if used instead of SMTP)
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
    USE_SENDGRID = bool(os.environ.get('USE_SENDGRID', False))
    
    # Application settings
    APP_NAME = 'نظام إدارة أعطال الأجهزة الطبية'  # Arabic name: Medical Device Fault Management System
    APP_NAME_EN = 'Medical Device Management'      # English name
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Default for first run only
    
    # Language settings
    DEFAULT_LANGUAGE = 'ar'  # Arabic is the default language
    LANGUAGES = ['ar', 'en']  # Supported languages: Arabic and English
    
    # AWS-inspired colors
    AWS_ORANGE = '#FF9900'
    AWS_WHITE = '#FFFFFF'
    AWS_GRAY = '#232F3E'
    
    # Mobile settings
    MOBILE_FRIENDLY = True
