import os
import logging
from flask import Flask, request, g, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
csrf = CSRFProtect()
login_manager = LoginManager()

# Create the application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")  # Use environment variable in production
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # Needed for url_for to generate with https

# Configure the database with UTF-8 support for Arabic text
db_uri = os.environ.get("DATABASE_URL", "sqlite:///medical_device_management.db")
if db_uri.startswith('postgresql://'):
    # Ensure PostgreSQL uses UTF-8 encoding
    if '?' not in db_uri:
        db_uri += '?client_encoding=utf8'
    else:
        db_uri += '&client_encoding=utf8'

app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "connect_args": {"options": "-c timezone=utc"}  # Set timezone to UTC for consistent timestamps
}

# Initialize the extensions with the app
db.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)

# Set up language support
from config import Config
app.config.from_object(Config)

# Import language helper
from lang import get_text, with_language

# Setup template context processor to make translations available in templates
@app.context_processor
def inject_language_functions():
    return {
        '_': get_text,
        'get_locale': lambda: session.get('language', Config.DEFAULT_LANGUAGE),
        'is_rtl': lambda: session.get('language', Config.DEFAULT_LANGUAGE) == 'ar',
        'languages': Config.LANGUAGES
    }

# Configure login manager
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Import models (after db initialization to avoid circular imports)
with app.app_context():
    # Import models and routes
    from models import User, Unit, Device, Report, Notification
    import routes
    
    # Create all tables in the database
    db.create_all()
    
    # Initialize database with sample data if it's empty
    from utils import initialize_db
    initialize_db()

# Import the routes to register them with the app
from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
