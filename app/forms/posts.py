from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    """A form that handles posts"""
    title = StringField('Title',
                        validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Content',
                            validators=[DataRequired(), Length(min=30)])
    submit = SubmitField('Submit')