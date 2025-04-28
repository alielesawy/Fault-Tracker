from app import app, db
from utils import initialize_db
from models import User, Unit, Device, Report, Notification

with app.app_context():
    # Force a connection to ensure the database is accessible
    engine = db.engine
    connection = engine.connect()
    connection.close()
    
    db.create_all()
    initialize_db()
    print("Database initialized successfully")