# Application Dependencies

## Python Packages

This application uses the following Python packages:

- **email-validator**: For email validation in forms
- **flask**: Web application framework
- **flask-login**: User authentication and session management
- **flask-sqlalchemy**: SQLAlchemy ORM integration for Flask
- **flask-wtf**: Form handling and CSRF protection
- **gunicorn**: WSGI HTTP server for production
- **itsdangerous**: Tools for secure token generation (used for password reset)
- **psycopg2-binary**: PostgreSQL adapter for Python
- **sendgrid**: SendGrid API client for email notifications
- **sqlalchemy**: SQL toolkit and ORM
- **werkzeug**: Web application utilities (used for password hashing)
- **wtforms**: Form validation and rendering

## Frontend Libraries

- **Bootstrap 4**: CSS framework for responsive design
- **jQuery**: JavaScript library
- **Chart.js**: JavaScript charting library for dashboard visualizations
- **Feather Icons**: Icon library

## System Requirements

- **Python 3.11+**
- **PostgreSQL 12+**: Database server with UTF-8 support
- **Web Server**: Nginx or similar (recommended for production)

## Development Tools

For development, the following tools are recommended:

- **Flask debug mode**: Enabled in development
- **Python debugging tools**: pdb or similar
- **Database management**: pgAdmin or similar PostgreSQL client
- **Text editor/IDE**: With Python and Flask support