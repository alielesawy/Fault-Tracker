import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app import db
from models import User, Unit, Device, Report, Notification
from config import Config

def admin_required(f):
    """Decorator for routes that require admin privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Admin':
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def send_email(subject, recipient, html_body):
    """Send an email using SMTP."""
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = Config.MAIL_DEFAULT_SENDER
    message['To'] = recipient
    
    # Attach HTML part
    part = MIMEText(html_body, 'html')
    message.attach(part)
    
    try:
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        server.starttls()
        
        # Log in if credentials are provided
        if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        
        server.sendmail(Config.MAIL_DEFAULT_SENDER, recipient, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def generate_reset_token(user):
    """Generate a token for password reset."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(user.email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    """Verify the password reset token."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
        return User.query.filter_by(email=email).first()
    except (BadSignature, SignatureExpired):
        return None

def send_password_reset_email(user):
    """Send password reset email to user."""
    token = generate_reset_token(user)
    reset_url = url_for('reset_password', token=token, _external=True)
    
    subject = f"{Config.APP_NAME} - Password Reset"
    html_body = f"""
    <p>Dear {user.name},</p>
    <p>To reset your password <a href="{reset_url}">click here</a>.</p>
    <p>Alternatively, you can paste the following link in your browser's address bar:</p>
    <p>{reset_url}</p>
    <p>If you have not requested a password reset simply ignore this message.</p>
    <p>Sincerely,</p>
    <p>The {Config.APP_NAME} Team</p>
    """
    
    return send_email(subject, user.email, html_body)

def send_fault_notification_email(user, report):
    """Send notification about a new fault report to a technician."""
    device = Device.query.get(report.device_id)
    unit = Unit.query.get(report.unit_id)
    
    subject = f"{Config.APP_NAME} - New Fault Report"
    html_body = f"""
    <p>Dear {user.name},</p>
    <p>A new fault report has been submitted:</p>
    <ul>
        <li><strong>Device:</strong> {device.device_name}</li>
        <li><strong>Serial Number:</strong> {report.serial_number or device.serial_number}</li>
        <li><strong>Unit:</strong> {unit.unit_name}</li>
        <li><strong>Description:</strong> {report.fault_description or 'No description provided'}</li>
        <li><strong>Reported at:</strong> {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
    </ul>
    <p>Please login to the system to review and respond to this report.</p>
    <p>Sincerely,</p>
    <p>The {Config.APP_NAME} Team</p>
    """
    
    # Record notification in database
    notification = Notification(
        report_id=report.report_id,
        user_id=user.user_id,
        email_content=html_body
    )
    db.session.add(notification)
    db.session.commit()
    
    return send_email(subject, user.email, html_body)

def initialize_db():
    """Initialize the database with sample data if it's empty."""
    # Check if database is already initialized
    if User.query.first() is not None:
        return
    
    # Add sample units
    unit1 = Unit(unit_name="Emergency Room", phone_numbers="123-456-7890")
    unit2 = Unit(unit_name="ICU", phone_numbers="123-456-7891")
    db.session.add(unit1)
    db.session.add(unit2)
    db.session.flush()  # Get IDs without committing
    
    # Add sample users
    admin = User(
        email=Config.ADMIN_EMAIL,
        name="Admin User",
        phone_number="123-456-7890",
        role="Admin"
    )
    admin.set_password(Config.ADMIN_PASSWORD)
    
    tech = User(
        email="tech@example.com",
        name="Tech User",
        phone_number="123-456-7891",
        role="Technician",
        unit_id=unit1.unit_id
    )
    tech.set_password("tech123")
    
    db.session.add(admin)
    db.session.add(tech)
    db.session.flush()
    
    # Add sample devices
    devices = [
        Device(
            serial_number="SN001",
            device_name="ECG Monitor",
            device_type="Monitoring",
            model="CardioMax 3000",
            unit_id=unit1.unit_id,
            category="Monitoring",
            origin_country="USA",
            status="Working",
            description="Cardiac monitoring device"
        ),
        Device(
            serial_number="SN002",
            device_name="Ventilator",
            device_type="Life Support",
            model="BreathAssist Pro",
            unit_id=unit2.unit_id,
            category="Life Support",
            origin_country="Germany",
            status="Working",
            description="Mechanical ventilation device"
        ),
        Device(
            serial_number="SN003",
            device_name="Infusion Pump",
            device_type="Therapeutic",
            model="FlowControl 200",
            unit_id=unit1.unit_id,
            category="Therapeutic",
            origin_country="Japan",
            status="Working",
            description="IV fluid and medication delivery"
        ),
        Device(
            serial_number="SN004",
            device_name="X-Ray Machine",
            device_type="Diagnostic",
            model="ClearView XR",
            unit_id=unit2.unit_id,
            category="Diagnostic",
            origin_country="USA",
            status="Working",
            description="Radiography imaging device"
        ),
        Device(
            serial_number="SN005",
            device_name="Patient Monitor",
            device_type="Monitoring",
            model="VitalTrack Pro",
            unit_id=unit1.unit_id,
            category="Monitoring",
            origin_country="Sweden",
            status="Faulty",
            description="Vital signs monitoring system"
        )
    ]
    
    for device in devices:
        db.session.add(device)
    
    # Commit all changes
    db.session.commit()
