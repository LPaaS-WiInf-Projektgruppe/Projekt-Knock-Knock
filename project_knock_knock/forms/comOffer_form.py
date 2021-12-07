from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp


class ComOfferForm(FlaskForm):
    von = StringField('from')
    nach = StringField('to')
    zeit_start = DateTimeField('start')
    zeit_ende = DateTimeField('end')
    geld = IntegerField('ct')
    dauer = IntegerField('days')
