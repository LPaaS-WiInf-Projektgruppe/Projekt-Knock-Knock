from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, IntegerRangeField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp


class RatingForm(FlaskForm):
    rating = IntegerRangeField('Rating', validators=[NumberRange(min=0, max=5)])
    submit = SubmitField("Save Rating")
