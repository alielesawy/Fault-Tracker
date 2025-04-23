import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///medical_device_management.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email settings (for Gmail SMTP)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@medicaldevices.com')
    
    # Application settings
    APP_NAME = 'Medical Device Management'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Default for first run only
    
    # AWS-inspired colors
    AWS_ORANGE = '#FF9900'
    AWS_WHITE = '#FFFFFF'
    AWS_GRAY = '#232F3E'
