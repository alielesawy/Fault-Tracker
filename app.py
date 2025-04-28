import os
import logging
from dotenv import load_dotenv  # Add this import
from flask import Flask, request, g, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Create the application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
db_uri = os.environ.get("DATABASE_URL", os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///medical_device_management.db"))
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
logger.debug(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db = SQLAlchemy(app, model_class=Base)
csrf = CSRFProtect()
login_manager = LoginManager()

# Initialize the extensions with the app
csrf.init_app(app)
login_manager.init_app(app)

# Set up language support
from config import Config
app.config.from_object(Config)

# Import language helper
from lang import get_text, with_language

# Define nl2br filter to convert newlines to <br> tags
def nl2br(value):
    if value:
        return value.replace('\n', '<br>')
    return ''
app.jinja_env.filters['nl2br'] = nl2br

# Setup template context processor
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

# Import models (after db initialization)
with app.app_context():
    from models import User, Unit, Device, Report, Notification

# Import and register routes after all other imports
from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)