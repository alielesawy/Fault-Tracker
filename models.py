from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False)  # 'Technician' or 'Admin'
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=True)
    
    # Relationships
    unit = db.relationship('Unit', backref='users')
    reports_resolved = db.relationship('Report', backref='technician', foreign_keys='Report.technician_id')
    notifications = db.relationship('Notification', backref='user')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Flask-Login interface methods
    def get_id(self):
        return str(self.user_id)


class Unit(db.Model):
    __tablename__ = 'units'
    
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(100), nullable=False, unique=True)
    phone_numbers = db.Column(db.String(100), nullable=True)
    
    # Relationships
    devices = db.relationship('Device', backref='unit')
    reports = db.relationship('Report', backref='unit')
    
    def __repr__(self):
        return f'<Unit {self.unit_name}>'


class Device(db.Model):
    __tablename__ = 'devices'
    
    device_id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    origin_country = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Working')
    description = db.Column(db.Text, nullable=True)
    
    # Relationships
    reports = db.relationship('Report', backref='device')
    
    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('serial_number', 'unit_id', name='unique_device_per_unit'),
    )
    
    def __repr__(self):
        return f'<Device {self.device_name} ({self.serial_number})>'


class Report(db.Model):
    __tablename__ = 'reports'
    
    report_id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.device_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    serial_number = db.Column(db.String(100), nullable=True)
    fault_description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    action_taken = db.Column(db.Text, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    
    # Relationships
    notifications = db.relationship('Notification', backref='report')
    
    def __repr__(self):
        return f'<Report {self.report_id} - {self.status}>'


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.report_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email_content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<Notification {self.notification_id} - Report {self.report_id}>'
