"""
The link between the python and the static files.
This file contains the input fields the user
will use to find the artist and song. Which will
be passed to the APIs and then our model for
recommendations. Flask_WTF escapes strings by
default.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Collect artist/title info from user
class LoginForm(FlaskForm):
    """
    These forms will exist on the home page and will
    be used to query inputs from the user.
    """
    artist = StringField('Artist', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Groove')
