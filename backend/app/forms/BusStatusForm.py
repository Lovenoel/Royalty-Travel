"""A file that handles setting up bus status."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired

class BusStatusForm(FlaskForm):
    """
    A Form for filling up the bus status
    """
    bus_number = StringField('Bus Number', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('On Time', 'On Time'),
        ('Delayed', 'Delayed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    updated = DateTimeField('Date & Time', format='%m/%d/%Y %H:%M', validators=[DataRequired()])
    submit = SubmitField('Add Bus')