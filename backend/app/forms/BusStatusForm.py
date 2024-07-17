from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class BusStatusForm(FlaskForm):
    bus_number = StringField('Bus Number', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('On Time', 'On Time'),
        ('Delayed', 'Delayed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Bus')