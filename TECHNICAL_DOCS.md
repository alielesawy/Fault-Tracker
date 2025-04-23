# Technical Documentation - Medical Device Fault Management System

This document provides technical information for developers working on the Medical Device Fault Management System.

## System Architecture

The application follows a Flask-based MVC architecture:

```
medical-device-system/
├── app.py             # Application initialization and configuration
├── config.py          # Configuration settings
├── main.py            # Entry point
├── models.py          # Database models (SQLAlchemy)
├── routes.py          # URL routes and view functions
├── forms.py           # Form definitions (Flask-WTF)
├── utils.py           # Utility functions
├── lang.py            # Language support utilities
├── translations.py    # Translation dictionaries
├── static/            # Static assets (CSS, JS, images)
└── templates/         # Jinja2 HTML templates
```

## Database Schema

The system uses SQLAlchemy ORM with the following models:

### User Model
```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False)  # 'Technician' or 'Admin'
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=True)
```

### Unit Model
```python
class Unit(db.Model):
    __tablename__ = 'units'
    
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(100), nullable=False, unique=True)
    phone_numbers = db.Column(db.String(100), nullable=True)
```

### Device Model
```python
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
```

### Report Model
```python
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
```

### Notification Model
```python
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.report_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email_content = db.Column(db.Text, nullable=False)
```

## Authentication System

The application uses Flask-Login for user authentication with the following features:

- Password hashing using Werkzeug's security functions
- Role-based access control (Admin and Technician roles)
- Password reset functionality with secure token generation
- Login session management

## Multilingual Support

The application supports bilingual functionality with Arabic and English:

- Translation dictionaries in `translations.py`
- Language selection and storage in session
- RTL/LTR layout switching based on language
- Dynamic text replacement throughout the UI

## Key Components

### Forms (`forms.py`)

The application uses Flask-WTF for form handling, including:

- LoginForm: User authentication
- RegistrationForm: User registration
- FaultReportForm: Reporting device faults
- ReportResponseForm: Technician responses to faults
- DeviceForm: Device management
- UnitForm: Unit management

### Routes (`routes.py`)

Main application routes include:

- Authentication routes (`/login`, `/logout`, `/register`)
- Fault reporting and management (`/fault_report`, `/report_list`, `/report/<id>`)
- Device management (`/device_list`, `/device_add`, `/device_edit/<id>`)
- Administrative functions (`/admin/dashboard`, `/admin/user_management`, etc.)

### Email Notifications (`utils.py`)

The system sends email notifications using:

- SendGrid API (preferred method)
- Fallback to SMTP if SendGrid is not configured
- Bilingual email templates (Arabic and English)

## Frontend Design

### Templates

- Base layout with RTL support (`layout.html`)
- Authentication templates (`login.html`, `register.html`, etc.)
- Fault management templates (`fault_report.html`, `report_list.html`, etc.)
- Admin dashboards (`admin/dashboard.html`, `admin/user_management.html`, etc.)

### Static Assets

- CSS: Bootstrap 4 with custom RTL overrides
- JavaScript: jQuery, Chart.js for data visualization
- Icons: Bootstrap Icons

## Security Considerations

- CSRF protection using Flask-WTF
- Password hashing with Werkzeug security
- Form validation to prevent injection attacks
- Role-based access control for routes
- Secure password reset with tokens

## API Endpoints

The application primarily uses server-rendered templates, but includes a few API endpoints for AJAX operations:

- `/api/units`: Get list of available units
- `/api/device_status/<id>`: Update device status
- `/api/stats/devices`: Get device statistics for charts

## Development Guidelines

### Adding a New Feature

1. Define models in `models.py` if needed
2. Create forms in `forms.py` if needed
3. Add routes in `routes.py`
4. Create templates in the `templates` directory
5. Add translations to `translations.py`
6. Update documentation

### Adding a New Language

1. Add language code to `LANGUAGES` list in `config.py`
2. Create translation entries in `translations.py`
3. Ensure all templates handle the new language

### Database Schema Changes

1. Make changes to model definitions in `models.py`
2. For simple additions, the changes will be applied automatically
3. For complex changes (removing columns, etc.), create a migration script

## Testing

To run tests:

```bash
python -m unittest discover tests
```

Key test modules:

- `tests/test_auth.py`: Authentication tests
- `tests/test_reports.py`: Fault reporting tests
- `tests/test_admin.py`: Admin functionality tests

## Common Issues and Solutions

### Database Encoding
PostgreSQL database must be configured with UTF-8 encoding to properly support Arabic:

```sql
CREATE DATABASE medical_device_management WITH ENCODING='UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8';
```

### RTL Text Issues
Ensure proper CSS directives are used for RTL text and layouts:

```css
[dir="rtl"] {
    text-align: right;
}
```

### Email Sending
If emails fail to send, check:
1. SendGrid API key is valid
2. SMTP server settings are correct
3. Network allows outgoing SMTP traffic

## Performance Optimization

For high-load deployments, consider:

1. Database indexing on frequently queried fields
2. Caching with Redis or Memcached
3. Static asset compression and CDN delivery
4. Increasing Gunicorn worker count based on server resources

## Security Recommendations

1. Use HTTPS in production with valid SSL certificates
2. Keep all dependencies updated regularly
3. Configure proper Content Security Policy headers
4. Implement rate limiting on authentication endpoints
5. Set secure and HTTP-only flags on cookies