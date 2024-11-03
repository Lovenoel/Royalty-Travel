from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class BusForm(FlaskForm):
    """A form that handles bus creation"""
    # number_plate = StringField('Number plate', validators=[DataRequired(), Length(min: int = 6, max: int = 8)])
    number_plate = StringField('Number plate', validators=[DataRequired(), Length(min = 6, max = 8)])
    capacity = StringField('Capacity', validators=[DataRequired()])
    model = StringField('Bus model', validators=[DataRequired()])
    location = StringField('Bus location', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ("On Time", "On Time"),
        ("Delayed", "Delayed"),
        ("Cancelled", "Cancelled"),
        ("Arrived", "Arrived"),
        ('Operational', 'Operational'),
        ('Maintenance', 'Under Maintenance')
    ],
    validate_choice=True
    )
    submit = SubmitField('Add Bus')


class TransportStatusForm(FlaskForm):
    location = StringField('Current Location', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    transport_mode = SelectField('Transport Mode', choices=[('bus', 'Bus'), ('taxi', 'Taxi'), ('other', 'Other')])
    submit = SubmitField('Check Status')
    