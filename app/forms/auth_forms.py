# RegistrationForm
# LoginForm
# 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.users import User

class RegistrationForm(FlaskForm):
    """Form for user registration"""    
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=15)])
    phone = StringField('Phone',
                        validators=[DataRequired(), Length(min=10, max=15)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Register as admin')
    submit = SubmitField('SIGN UP')


    def validate_username(self, username):
        """ checks the availability of the username """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another')
        
    def validate_email(self, email):
        """ checks the availability of the username """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another')
    

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')