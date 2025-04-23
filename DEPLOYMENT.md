# Deployment Guide for Medical Device Fault Management System

This document provides a step-by-step guide for deploying the Medical Device Fault Management System in different environments.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Production Deployment](#production-deployment)
3. [Configuration Options](#configuration-options)
4. [Environment Variables](#environment-variables)
5. [Database Migration](#database-migration)
6. [SSL/TLS Configuration](#ssltls-configuration)
7. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Git

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd medical-device-management
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/medical_device_management
   SESSION_SECRET=your_secure_secret_key
   ```

5. **Run the application**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Production Deployment

### Prerequisites

- A server running Ubuntu 20.04+ or similar Linux distribution
- PostgreSQL 12+
- Nginx
- Domain name (optional, but recommended)
- Let's Encrypt SSL certificate (optional, but recommended)

### Server Setup

1. **Update your server and install dependencies**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo apt install python3 python3-pip python3-venv postgresql nginx certbot python3-certbot-nginx
   ```

2. **Create a system user for the application**:
   ```bash
   sudo useradd -m -s /bin/bash medicalapp
   sudo su - medicalapp
   ```

3. **Clone the repository**:
   ```bash
   git clone <repository-url> ~/medical-device-system
   cd ~/medical-device-system
   ```

4. **Set up the virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Configure PostgreSQL**:
   ```bash
   sudo -u postgres psql
   ```
   In the PostgreSQL shell:
   ```sql
   CREATE USER medicalapp WITH PASSWORD 'secure_password';
   CREATE DATABASE medical_device_management WITH OWNER medicalapp ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
   GRANT ALL PRIVILEGES ON DATABASE medical_device_management TO medicalapp;
   \q
   ```

6. **Create a systemd service**:
   Create a file `/etc/systemd/system/medical-device-app.service`:
   ```ini
   [Unit]
   Description=Medical Device Management Application
   After=network.target postgresql.service

   [Service]
   User=medicalapp
   Group=medicalapp
   WorkingDirectory=/home/medicalapp/medical-device-system
   Environment="PATH=/home/medicalapp/medical-device-system/venv/bin"
   Environment="DATABASE_URL=postgresql://medicalapp:secure_password@localhost:5432/medical_device_management"
   Environment="SESSION_SECRET=your_secure_secret_key"
   ExecStart=/home/medicalapp/medical-device-system/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Configure Nginx**:
   Create a file `/etc/nginx/sites-available/medical-device-app`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Enable the Nginx site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/medical-device-app /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **Start the application service**:
   ```bash
   sudo systemctl start medical-device-app
   sudo systemctl enable medical-device-app
   ```

## Configuration Options

The application can be configured through environment variables or by modifying the `config.py` file. Here are some of the key configuration options:

- **Language Settings**: 
  - Default language is Arabic (`ar`)
  - Supported languages: Arabic (`ar`) and English (`en`)
  - To change default, modify `DEFAULT_LANGUAGE` in `config.py`

- **Email Settings**:
  - SendGrid API (preferred) or SMTP server
  - Configure in `config.py` or through environment variables

- **Authentication**:
  - Default admin account is created on first run
  - Password reset functionality is enabled by default
  - Session duration can be configured in `config.py`

## Environment Variables

| Variable Name | Description | Default Value |
|---------------|-------------|---------------|
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///medical_device_management.db` |
| `SESSION_SECRET` | Secret key for session security | `dev-secret-key` (Change in production!) |
| `SENDGRID_API_KEY` | API key for SendGrid email service | None |
| `USE_SENDGRID` | Whether to use SendGrid for emails | `False` |
| `MAIL_SERVER` | SMTP server address | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP server port | `587` |
| `MAIL_USERNAME` | SMTP username | None |
| `MAIL_PASSWORD` | SMTP password | None |
| `MAIL_DEFAULT_SENDER` | Default email sender | `noreply@medicaldevices.com` |
| `ADMIN_EMAIL` | Admin user email | `admin@example.com` |
| `ADMIN_PASSWORD` | Admin user password | `admin123` (Change in production!) |
| `DEFAULT_LANGUAGE` | Default language code | `ar` (Arabic) |

## Database Migration

The application automatically creates the necessary database tables on first run. If you need to make changes to the database schema:

1. Stop the application
2. Make changes to the models in `models.py`
3. Restart the application - tables will be updated (Note: this works for adding columns, but not for removing them)

For more complex migrations, consider using Alembic with Flask-Migrate.

## SSL/TLS Configuration

To enable HTTPS (recommended for production):

```bash
sudo certbot --nginx -d your-domain.com
```

Certbot will modify your Nginx configuration to enable HTTPS.

## Troubleshooting

### Database Connection Issues

- Verify that PostgreSQL is running:
  ```bash
  sudo systemctl status postgresql
  ```
- Check PostgreSQL logs:
  ```bash
  sudo tail -f /var/log/postgresql/postgresql-*.log
  ```
- Verify connection string format:
  ```
  postgresql://username:password@host:port/database
  ```

### Application Not Starting

- Check the application logs:
  ```bash
  sudo journalctl -u medical-device-app
  ```
- Verify that all dependencies are installed:
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Ensure that the system service is configured correctly:
  ```bash
  sudo systemctl cat medical-device-app
  ```

### Email Sending Issues

- If using SendGrid, verify your API key is correct
- For SMTP, check server settings and credentials
- Test email configuration:
  ```bash
  python -c "from utils import send_email; send_email('Test Subject', 'recipient@example.com', '<p>Test content</p>')"
  ```

### Performance Tuning

- Adjust the number of Gunicorn workers based on server resources:
  ```
  ExecStart=/path/to/gunicorn --workers <2 x num_cores + 1> --bind 0.0.0.0:5000 main:app
  ```
- Consider setting up database connection pooling
- For high-traffic sites, add a caching layer with Redis