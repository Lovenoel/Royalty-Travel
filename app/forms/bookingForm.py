"""
A booking form
"""

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class BookingForm(FlaskForm):
    """Booking Form"""
    username  = StringField('Username', validators=[DataRequired('Username is required')])
    passeneger_name = StringField('Passenger Name', validators=[DataRequired()])
    departure_place = StringField('Departuure Place', validators=[DataRequired()])
    destination = StringField('Destianation', validators=[DataRequired()])
    departure_data_time = DateTimeField('Date & Time', format='%m/%d/%Y %H:%M', validators=[DataRequired()])
    submit = SubmitField('Book Now')
    