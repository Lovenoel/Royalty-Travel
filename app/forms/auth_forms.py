# RegistrationForm
# LoginForm
# 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from models.users import User

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    name = StringField('Name',
                       validators=[DataRequired()])
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


class UpdateForm(FlaskForm):
    """Form responsible for updating the user page."""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    # profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif'])])
    favorite_color = StringField('Favorite Color')
    about_author = TextAreaField('About Author')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """ checks the diffrence of the username """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another')
        
    def validate_email(self, email):
        """ checks the difference of the user email """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another')
            

class NamerForm(FlaskForm):
    """Form for name registration."""
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")