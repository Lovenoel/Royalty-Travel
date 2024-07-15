from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import Passenger

class PassengerForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone',
                        validators=[DataRequired(),
                                    Length(min=10, max=15)])
    addPassenger = SubmitField('Add Passenger')


    def validate_passenger_name(self, username):
        """ checks the availability of the username """
        passenger = Passenger.query.filter_by(username=username.data).first()
        if passenger:
            raise ValidationError('That Passenger name is taken. Please choose another')
        
    def validate_email(self, email):
        """ checks the availability of the username """
        passenger = Passenger.query.filter_by(email=email.data).first()
        if passenger:
            raise ValidationError('That email is taken. Please choose another')