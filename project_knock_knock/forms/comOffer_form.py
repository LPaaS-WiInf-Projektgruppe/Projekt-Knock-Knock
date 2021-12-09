from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

GELD_ERROR = "Please enter a a valid amount of money! (Must be a number und have a maximum amount of 2 decimal places: e.g 12.99 Euro) "
LOCATION_ERROR = "Please enter a valid location! (Must be an actual place in the format: street + number)"
TIME_ERROR = "Please enter a valid time! (Must be in the format DD.MM.YYYY-HH:MM and can't be in the past)"
DURATION_ERROR = "Must be a valid duration! (Must be a number and have a maximum amount of 1 decimal place: e.g. 1.5. Furthermore duration has to be be larger than 0 and smaller than 7 in order to be accepted.) "

#"^[A-z]*$"
location_validator = Regexp("^[A-z]*\s?[0-9]{0,3}$", 0, message = LOCATION_ERROR)

#"^[0-9]*\.[0-9][0-9]$"
geld_validator = Regexp("^[0-9]*\.[0-9][0-9]$", 0, message = GELD_ERROR)

#"^([0-9][0-9])\:([0-9][0-9])$"
zeit_validator = Regexp("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9]\s[0-9][0-9]\:[0-9][0-9]$", 0, message = TIME_ERROR)

#"^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]\s[0-9][0-9]\:[0-9][0-9]$"
#zeit_validator = Regexp("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]\s[0-9][0-9]\:[0-9][0-9]$", 0, message = TIME_ERROR)

#"^[0-9]{1,2}$"
dauer_validator = Regexp("^[0-9]{1,2}$", 0, message = DURATION_ERROR)

class ComOfferForm(FlaskForm):
    von = StringField('from', validators= [location_validator])
    nach = StringField('to', validators= [location_validator])
    zeit_start = StringField('gewünschte Zeit', validators= [zeit_validator])
    zeit_ende = StringField('bis (optional)', validators= [zeit_validator])
    geld = StringField('Kilometerpreis', validators = [geld_validator])
    dauer = StringField('Dauer in Tagen', validators= [dauer_validator])
    submit = SubmitField('Create Offer')
