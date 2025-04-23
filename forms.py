from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from models import User, Unit, Device

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Technician', 'Technician'), ('Admin', 'Admin')], validators=[DataRequired()])
    unit_id = SelectField('Unit', coerce=int, validators=[Optional()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.unit_id.choices = [(0, 'None')] + [(u.unit_id, u.unit_name) for u in Unit.query.all()]

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(min=10, max=20)])
    submit = SubmitField('Update Profile')

class FaultReportForm(FlaskForm):
    unit_id = SelectField('Unit', coerce=int, validators=[DataRequired()])
    device_name = StringField('Device Name', validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[Optional()])
    fault_description = TextAreaField('Fault Description', validators=[Optional()])
    submit = SubmitField('Submit Report')
    
    def __init__(self, *args, **kwargs):
        super(FaultReportForm, self).__init__(*args, **kwargs)
        self.unit_id.choices = [(u.unit_id, u.unit_name) for u in Unit.query.all()]

class ReportResponseForm(FlaskForm):
    action_taken = TextAreaField('Action Taken', validators=[DataRequired()])
    photo_report = FileField('Technical Report Photo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Images and PDF only!')
    ])
    submit = SubmitField('Submit Response')

class DeviceForm(FlaskForm):
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    device_name = StringField('Device Name', validators=[DataRequired()])
    device_type = StringField('Device Type', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    unit_id = SelectField('Unit', coerce=int, validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Diagnostic', 'Diagnostic'), 
        ('Therapeutic', 'Therapeutic'),
        ('Monitoring', 'Monitoring'),
        ('Life Support', 'Life Support'),
        ('Laboratory', 'Laboratory'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    origin_country = StringField('Origin Country', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('Working', 'Working'),
        ('Faulty', 'Faulty'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Out of Service', 'Out of Service')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Device')
    
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.unit_id.choices = [(u.unit_id, u.unit_name) for u in Unit.query.all()]

class UnitForm(FlaskForm):
    unit_name = StringField('Unit Name', validators=[DataRequired()])
    phone_numbers = StringField('Phone Numbers', validators=[Optional()])
    submit = SubmitField('Save Unit')

class ReportGenerationForm(FlaskForm):
    report_type = SelectField('Report Type', choices=[
        ('fault_reports', 'Fault Reports'),
        ('device_inventory', 'Device Inventory')
    ], validators=[DataRequired()])
    start_date = StringField('Start Date', validators=[Optional()])
    end_date = StringField('End Date', validators=[Optional()])
    submit = SubmitField('Generate Report')
