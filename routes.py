from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask import render_template, redirect, url_for, flash, request, jsonify, abort, session
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
import pandas as pd
import os
from app import db, login_manager
from models import User, Unit, Device, Report, Notification
from forms import (
    LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm,
    ProfileForm, FaultReportForm, ReportResponseForm, DeviceForm, UnitForm,
    ReportGenerationForm, DeviceFilterForm, ExcelUploadForm
)
from wtforms.validators import Optional, EqualTo
from utils import admin_required, send_password_reset_email, send_fault_notification_email
from lang import set_locale, with_language, get_locale
from config import Config

bp = Blueprint('main', __name__)

def register_routes(app):
    
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    # Set Arabic as the default language for all routes
    @app.before_request
    @with_language
    def before_request():
        # If no language is set in session, set it to default (Arabic)
        if 'language' not in session:
            set_locale(Config.DEFAULT_LANGUAGE)
    
    # Route to change language
    @app.route('/set_language/<lang>')
    def set_language(lang):
        # Validate language
        if lang in Config.LANGUAGES:
            set_locale(lang)
        return redirect(request.referrer or url_for('index'))
    
    @app.route('/')
    def index():
        return render_template('index.html', title='Home')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password', 'danger')
                return redirect(url_for('login'))
            
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or next_page.startswith('/'):
                if user.role == 'Admin':
                    next_page = url_for('admin_dashboard')
                else:
                    next_page = url_for('report_list')
                    
            return redirect(next_page)
        
        return render_template('login.html', title='Sign In', form=form)
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/register', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                name=form.name.data,
                phone_number=form.phone_number.data,
                role=form.role.data,
                unit_id=form.unit_id.data if form.unit_id.data != 0 else None
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User has been registered successfully!', 'success')
            return redirect(url_for('admin_user_management'))
        
        return render_template('register.html', title='Register User', form=form)
    
    @app.route('/reset_password_request', methods=['GET', 'POST'])
    def reset_password_request():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
            flash('Check your email for instructions to reset your password', 'info')
            return redirect(url_for('login'))
        
        return render_template('reset_password_request.html', title='Reset Password', form=form)
    
    @app.route('/reset_password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        user = User.verify_reset_password_token(token)
        if not user:
            flash('Invalid or expired token', 'danger')
            return redirect(url_for('reset_password_request'))
        
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your password has been reset.', 'success')
            return redirect(url_for('login'))
        
        return render_template('reset_password.html', title='Reset Password', form=form)
    
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm()
        if request.method == 'GET':
            form.name.data = current_user.name
            form.phone_number.data = current_user.phone_number
        
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.phone_number = form.phone_number.data
            db.session.commit()
            flash('Your profile has been updated.', 'success')
            return redirect(url_for('profile'))
        
        return render_template('profile.html', title='Profile', form=form)
    
    @app.route('/fault_report', methods=['GET', 'POST'])
    def fault_report():
        # Only allow non-logged in users to access the fault report form
        if current_user.is_authenticated:
            flash('Logged in users should use the admin interface to manage faults.', 'info')
            return redirect(url_for('index'))
            
        form = FaultReportForm()
        if form.validate_on_submit():
            # Check if device exists
            device = Device.query.filter_by(
                device_name=form.device_name.data,
                unit_id=form.unit_id.data
            ).first()
            
            # If device doesn't exist, create it
            if not device:
                device = Device(
                    serial_number=form.serial_number.data or "Unknown",
                    device_name=form.device_name.data,
                    device_type="Unspecified",
                    model="Unspecified",
                    unit_id=form.unit_id.data,
                    category="Unspecified",
                    status="Faulty",
                    description="Automatically created from fault report"
                )
                db.session.add(device)
                db.session.flush()  # Get device_id without committing
            
            # Create report
            report = Report(
                device_id=device.device_id,
                unit_id=form.unit_id.data,
                serial_number=form.serial_number.data,
                fault_description=form.fault_description.data,
                created_at=datetime.utcnow(),
                status='Pending'
            )
            db.session.add(report)
            db.session.commit()
            
            # Send email notification to all technicians
            technicians = User.query.filter_by(role='Technician').all()
            for tech in technicians:
                send_fault_notification_email(tech, report)
            
            flash('Fault report submitted successfully!', 'success')
            return redirect(url_for('index'))
        
        return render_template('fault_report.html', title='Report a Fault', form=form)
    
    @app.route('/report_list')
    @login_required
    def report_list():
        # Get reports with pagination
        page = request.args.get('page', 1, type=int)
        reports = Report.query.order_by(Report.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        
        return render_template('report_list.html', title='Fault Reports', reports=reports)
    
    @app.route('/report/<int:report_id>', methods=['GET', 'POST'])
    @login_required
    def report_detail(report_id):
        report = Report.query.get_or_404(report_id)
        form = ReportResponseForm()
        
        if form.validate_on_submit():
            report.action_taken = form.action_taken.data
            report.resolved_at = datetime.utcnow()
            report.status = 'Resolved'
            report.technician_id = current_user.user_id
            
            # Handle file upload
            if form.photo_report.data:
                # Create uploads directory if it doesn't exist
                uploads_dir = os.path.join(os.getcwd(), 'static', 'uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                
                # Generate a unique filename with timestamp
                filename = f"report_{report_id}_{int(datetime.now().timestamp())}"
                file_ext = os.path.splitext(form.photo_report.data.filename)[1]
                safe_filename = filename + file_ext
                
                # Save the file
                filepath = os.path.join(uploads_dir, safe_filename)
                form.photo_report.data.save(filepath)
                
                # Save the relative path to the database
                report.photo_report = os.path.join('uploads', safe_filename)
            
            db.session.commit()
            flash('Response submitted successfully!', 'success')
            return redirect(url_for('report_list'))
        
        return render_template('report_detail.html', title='Report Details', report=report, form=form)
    
    @app.route('/device_list', methods=['GET', 'POST'])
    @login_required
    def device_list():
        form = DeviceFilterForm(request.args)
        
        # Build query with filters
        query = Device.query
        
        # Apply filters if form is submitted
        if request.args:
            # Filter by unit
            if form.unit_id.data and form.unit_id.data != 0:
                query = query.filter(Device.unit_id == form.unit_id.data)
            
            # Filter by category
            if form.category.data:
                query = query.filter(Device.category == form.category.data)
            
            # Filter by status
            if form.status.data:
                query = query.filter(Device.status == form.status.data)
            
            # Filter by model (partial match)
            if form.model.data:
                query = query.filter(Device.model.ilike(f'%{form.model.data}%'))
            
            # Filter by manufacturer/country (partial match)
            if form.origin_country.data:
                query = query.filter(Device.origin_country.ilike(f'%{form.origin_country.data}%'))
            
            # General search across multiple fields
            if form.search.data:
                search_term = f"%{form.search.data}%"
                query = query.filter(
                    (Device.device_name.ilike(search_term)) | 
                    (Device.device_type.ilike(search_term)) |
                    (Device.serial_number.ilike(search_term)) |
                    (Device.description.ilike(search_term))
                )
        
        # Get devices with pagination
        page = request.args.get('page', 1, type=int)
        devices = query.order_by(Device.device_name).paginate(
            page=page, per_page=10, error_out=False
        )
        
        return render_template('device_list.html', title='Device List', devices=devices, form=form)
    
    @app.route('/device_add', methods=['GET', 'POST'])
    @login_required
    def device_add():
        form = DeviceForm()
        if form.validate_on_submit():
            # Check if device already exists
            existing_device = Device.query.filter_by(
                serial_number=form.serial_number.data,
                unit_id=form.unit_id.data
            ).first()
            
            if existing_device:
                flash('A device with this serial number already exists in the selected unit.', 'danger')
                return redirect(url_for('device_add'))
            
            device = Device(
                serial_number=form.serial_number.data,
                device_name=form.device_name.data,
                device_type=form.device_type.data,
                model=form.model.data,
                unit_id=form.unit_id.data,
                category=form.category.data,
                origin_country=form.origin_country.data,
                status=form.status.data,
                description=form.description.data
            )
            db.session.add(device)
            db.session.commit()
            flash('Device added successfully!', 'success')
            return redirect(url_for('device_list'))
        
        return render_template('device_add.html', title='Add Device', form=form)
        
    @app.route('/device_import', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def device_import():
        form = ExcelUploadForm()
        
        if form.validate_on_submit():
            # Save the uploaded file temporarily
            uploaded_file = form.excel_file.data
            file_path = os.path.join(os.getcwd(), 'temp_import.xlsx')
            uploaded_file.save(file_path)
            
            try:
                # Read Excel file
                df = pd.read_excel(file_path)
                
                # Required columns
                required_columns = ['serial_number', 'device_name', 'device_type', 'model', 
                                   'unit_name', 'category', 'status']
                
                # Validate columns
                for col in required_columns:
                    if col not in df.columns:
                        flash(f'Column {col} is missing in the Excel file.', 'danger')
                        return redirect(url_for('device_import'))
                
                success_count = 0
                error_count = 0
                
                # Process each row
                for index, row in df.iterrows():
                    try:
                        # Find unit by name
                        unit = Unit.query.filter_by(unit_name=row['unit_name']).first()
                        
                        # Skip if unit doesn't exist
                        if not unit:
                            error_count += 1
                            continue
                        
                        # Check if device already exists
                        existing_device = Device.query.filter_by(
                            serial_number=row['serial_number'],
                            unit_id=unit.unit_id
                        ).first()
                        
                        if existing_device:
                            # Update existing device
                            existing_device.device_name = row['device_name']
                            existing_device.device_type = row['device_type']
                            existing_device.model = row['model']
                            existing_device.category = row['category']
                            existing_device.status = row['status']
                            
                            # Optional columns
                            if 'origin_country' in df.columns and not pd.isna(row['origin_country']):
                                existing_device.origin_country = row['origin_country']
                            
                            if 'description' in df.columns and not pd.isna(row['description']):
                                existing_device.description = row['description']
                                
                            success_count += 1
                            
                        else:
                            # Create new device
                            device = Device(
                                serial_number=row['serial_number'],
                                device_name=row['device_name'],
                                device_type=row['device_type'],
                                model=row['model'],
                                unit_id=unit.unit_id,
                                category=row['category'],
                                status=row['status']
                            )
                            
                            # Optional columns
                            if 'origin_country' in df.columns and not pd.isna(row['origin_country']):
                                device.origin_country = row['origin_country']
                            
                            if 'description' in df.columns and not pd.isna(row['description']):
                                device.description = row['description']
                                
                            db.session.add(device)
                            success_count += 1
                            
                    except Exception as e:
                        error_count += 1
                        
                # Commit all changes
                db.session.commit()
                
                # Clean up the temporary file
                os.remove(file_path)
                
                if error_count > 0:
                    flash(f'Imported {success_count} devices with {error_count} errors.', 'warning')
                else:
                    flash(f'Successfully imported {success_count} devices.', 'success')
                    
                return redirect(url_for('device_list'))
                
            except Exception as e:
                flash(f'Error processing Excel file: {str(e)}', 'danger')
                # Clean up in case of error
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
        return render_template('device_import.html', title='Import Devices', form=form)
    
    @app.route('/device_edit/<int:device_id>', methods=['GET', 'POST'])
    @login_required
    def device_edit(device_id):
        device = Device.query.get_or_404(device_id)
        form = DeviceForm(obj=device)
        
        if form.validate_on_submit():
            # Check if another device with same serial and unit exists
            existing_device = Device.query.filter(
                Device.serial_number == form.serial_number.data,
                Device.unit_id == form.unit_id.data,
                Device.device_id != device_id
            ).first()
            
            if existing_device:
                flash('Another device with this serial number already exists in the selected unit.', 'danger')
                return redirect(url_for('device_edit', device_id=device_id))
            
            device.serial_number = form.serial_number.data
            device.device_name = form.device_name.data
            device.device_type = form.device_type.data
            device.model = form.model.data
            device.unit_id = form.unit_id.data
            device.category = form.category.data
            device.origin_country = form.origin_country.data
            device.status = form.status.data
            device.description = form.description.data
            
            db.session.commit()
            flash('Device updated successfully!', 'success')
            return redirect(url_for('device_list'))
        
        # Pre-populate form for GET request
        if request.method == 'GET':
            form.serial_number.data = device.serial_number
            form.device_name.data = device.device_name
            form.device_type.data = device.device_type
            form.model.data = device.model
            form.unit_id.data = device.unit_id
            form.category.data = device.category
            form.origin_country.data = device.origin_country
            form.status.data = device.status
            form.description.data = device.description
            
        return render_template('device_edit.html', title='Edit Device', form=form, device=device)
    
    @app.route('/admin/dashboard')
    @login_required
    @admin_required
    def admin_dashboard():
        # Get statistics for dashboard
        total_devices = Device.query.count()
        working_devices = Device.query.filter_by(status='Working').count()
        faulty_devices = Device.query.filter_by(status='Faulty').count()
        pending_reports = Report.query.filter_by(status='Pending').count()
        resolved_reports = Report.query.filter_by(status='Resolved').count()
        
        # Get device categories - convert to serializable format
        device_categories_query = db.session.query(
            Device.category, func.count(Device.device_id)
        ).group_by(Device.category).all()
        
        # Convert SQLAlchemy Row objects to a serializable format
        device_categories = [{'category': category, 'count': count} for category, count in device_categories_query]
        
        # Get units
        units = Unit.query.all()
        
        # Get recent reports
        recent_reports = Report.query.order_by(Report.created_at.desc()).limit(5).all()
        
        return render_template(
            'admin/dashboard.html', 
            title='Admin Dashboard',
            total_devices=total_devices,
            working_devices=working_devices,
            faulty_devices=faulty_devices,
            pending_reports=pending_reports,
            resolved_reports=resolved_reports,
            device_categories=device_categories,
            units=units,
            recent_reports=recent_reports
        )
    
    @app.route('/admin/user_management')
    @login_required
    @admin_required
    def admin_user_management():
        users = User.query.all()
        return render_template('admin/user_management.html', title='User Management', users=users)
    
    @app.route('/admin/unit_management', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def admin_unit_management():
        form = UnitForm()
        units = Unit.query.all()
        
        if form.validate_on_submit():
            # Check if unit already exists
            existing_unit = Unit.query.filter_by(unit_name=form.unit_name.data).first()
            if existing_unit:
                flash('A unit with this name already exists.', 'danger')
                return redirect(url_for('admin_unit_management'))
            
            unit = Unit(
                unit_name=form.unit_name.data,
                phone_numbers=form.phone_numbers.data
            )
            db.session.add(unit)
            db.session.commit()
            flash('Unit added successfully!', 'success')
            return redirect(url_for('admin_unit_management'))
        
        return render_template('admin/unit_management.html', title='Unit Management', form=form, units=units)
    
    @app.route('/admin/edit_unit/<int:unit_id>', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def admin_edit_unit(unit_id):
        unit = Unit.query.get_or_404(unit_id)
        form = UnitForm(obj=unit)
        
        if form.validate_on_submit():
            # Check if another unit with same name exists
            existing_unit = Unit.query.filter(
                Unit.unit_name == form.unit_name.data,
                Unit.unit_id != unit_id
            ).first()
            
            if existing_unit:
                flash('Another unit with this name already exists.', 'danger')
                return redirect(url_for('admin_edit_unit', unit_id=unit_id))
            
            unit.unit_name = form.unit_name.data
            unit.phone_numbers = form.phone_numbers.data
            db.session.commit()
            flash('Unit updated successfully!', 'success')
            return redirect(url_for('admin_unit_management'))
        
        # Pre-populate form for GET request
        if request.method == 'GET':
            form.unit_name.data = unit.unit_name
            form.phone_numbers.data = unit.phone_numbers
            
        return render_template('admin/unit_management.html', title='Edit Unit', form=form, edit_unit=unit, units=Unit.query.all())
    
    @app.route('/admin/delete_unit/<int:unit_id>', methods=['POST'])
    @login_required
    @admin_required
    def admin_delete_unit(unit_id):
        unit = Unit.query.get_or_404(unit_id)
        
        # Check if unit has associated devices or reports
        if unit.devices or unit.reports or unit.users:
            flash('Cannot delete unit that has associated devices, reports, or users.', 'danger')
            return redirect(url_for('admin_unit_management'))
        
        db.session.delete(unit)
        db.session.commit()
        flash('Unit deleted successfully!', 'success')
        return redirect(url_for('admin_unit_management'))
    
    @app.route('/admin/reports', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def admin_reports():
        form = ReportGenerationForm()
        report_data = None
        report_type = None
        
        if form.validate_on_submit():
            report_type = form.report_type.data
            
            if report_type == 'fault_reports':
                # Get fault reports within date range
                query = db.session.query(
                    Report, Device, Unit, User
                ).join(
                    Device, Report.device_id == Device.device_id
                ).join(
                    Unit, Report.unit_id == Unit.unit_id
                ).outerjoin(
                    User, Report.technician_id == User.user_id
                )
                
                # Apply date filters if provided
                if form.start_date.data:
                    start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d')
                    query = query.filter(Report.created_at >= start_date)
                
                if form.end_date.data:
                    end_date = datetime.strptime(form.end_date.data + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
                    query = query.filter(Report.created_at <= end_date)
                
                report_data = query.order_by(Report.created_at.desc()).all()
                
            elif report_type == 'device_inventory':
                # Get device inventory report
                query = db.session.query(
                    Device, Unit
                ).join(
                    Unit, Device.unit_id == Unit.unit_id
                )
                
                report_data = query.order_by(Unit.unit_name, Device.device_name).all()
                
                # Get summary data
                device_by_type = db.session.query(
                    Device.device_type, func.count(Device.device_id)
                ).group_by(Device.device_type).all()
                
                device_by_status = db.session.query(
                    Device.status, func.count(Device.device_id)
                ).group_by(Device.status).all()
                
                device_by_category = db.session.query(
                    Device.category, func.count(Device.device_id)
                ).group_by(Device.category).all()
                
                # Convert to serializable format
                devices_list = [(device, unit) for device, unit in report_data]
                
                by_type_list = [{'type': type_name, 'count': count} for type_name, count in device_by_type]
                by_status_list = [{'status': status_name, 'count': count} for status_name, count in device_by_status]
                by_category_list = [{'category': category_name, 'count': count} for category_name, count in device_by_category]
                
                # Add summary data to report_data
                report_data = {
                    'devices': devices_list,
                    'by_type': by_type_list,
                    'by_status': by_status_list,
                    'by_category': by_category_list
                }
        
        return render_template('admin/reports.html', title='Reports', form=form, report_data=report_data, report_type=report_type)
    
    @app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def admin_edit_user(user_id):
        user = User.query.get_or_404(user_id)
        form = RegistrationForm(obj=user)
        
        # Remove password validation for edit by setting optional validators
        form.password.validators = [Optional()]
        form.password2.validators = [Optional(), EqualTo('password')]
        
        if form.validate_on_submit():
            # Check if another user with same email exists
            existing_user = User.query.filter(
                User.email == form.email.data,
                User.user_id != user_id
            ).first()
            
            if existing_user:
                flash('Another user with this email already exists.', 'danger')
                return redirect(url_for('admin_edit_user', user_id=user_id))
            
            user.email = form.email.data
            user.name = form.name.data
            user.phone_number = form.phone_number.data
            user.role = form.role.data
            user.unit_id = form.unit_id.data if form.unit_id.data != 0 else None
            
            # Update password if provided
            if form.password.data:
                user.set_password(form.password.data)
            
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin_user_management'))
        
        # Pre-populate form for GET request
        if request.method == 'GET':
            form.email.data = user.email
            form.name.data = user.name
            form.phone_number.data = user.phone_number
            form.role.data = user.role
            form.unit_id.data = user.unit_id if user.unit_id else 0
            
        return render_template('register.html', title='Edit User', form=form, edit_user=True)
    
    @app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
    @login_required
    @admin_required
    def admin_delete_user(user_id):
        user = User.query.get_or_404(user_id)
        
        # Check if user has associated reports
        if user.reports_resolved:
            flash('Cannot delete user who has resolved reports.', 'danger')
            return redirect(url_for('admin_user_management'))
        
        # Delete associated notifications
        Notification.query.filter_by(user_id=user_id).delete()
        
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('admin_user_management'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500