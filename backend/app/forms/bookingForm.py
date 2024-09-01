# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class BookingForm(FlaskForm):
    """Form for booking a bus ticket."""
    username = StringField('Username', validators=[DataRequired()])
    passenger_name = StringField('Passenger Name', validators=[DataRequired()])
    departure_place = StringField('Departure Place', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    date_time = DateTimeField('Date & Time', format='%m/%d/%Y %H:%M', validators=[DataRequired()])
    fare = StringField('Fare', validators=[DataRequired()])
    submit = SubmitField('Book Now')
