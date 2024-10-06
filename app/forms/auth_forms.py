# RegistrationForm
# LoginForm
# 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
