from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, SelectField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

select_choices = {1:"1", 2:"2", 3:"3", 4:"4", 5:"5"}
class RatingForm(FlaskForm):
    rating = SelectField('Rating', validators=[NumberRange(min=0, max=5)], choices = select_choices, coerce=int)
    submit = SubmitField("Save Rating")
