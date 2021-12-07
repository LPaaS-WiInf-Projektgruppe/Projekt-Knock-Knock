from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

GELD_ERROR = "Please enter a a valid amount of money e.g '12.99' "
LOCATION_ERROR = "locationerror "
TIME_ERROR = "time_error "
DURATION_ERROR = "durationerror "

location_validator = Regexp("^[A-z]*$", 0, message = LOCATION_ERROR)

geld_validator = Regexp("^[0-9]*\.[0-9][0-9]$", 0, message = GELD_ERROR)

zeit_validator = Regexp("^([0-9][0-9])\:([0-9][0-9])$", 0, message = TIME_ERROR)

zeit_validator = Regexp("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]\s[0-9][0-9]\:[0-9][0-9]$", 0, message = TIME_ERROR)

dauer_validator = Regexp("^[0-9]{1,2}$", 0, message = DURATION_ERROR)

class ComOfferForm(FlaskForm):
    von = StringField('from', validators= [location_validator])
    nach = StringField('to', validators= [location_validator])
    zeit_start = StringField('gewünschte Zeit', validators= [zeit_validator])
    zeit_ende = StringField('bis')
    geld = StringField(
        'Kilometerpreis',
        validators = [geld_validator]
    )
    dauer = StringField('Dauer in Tagen', validators= [dauer_validator])
    submit = SubmitField('Create Offer')
