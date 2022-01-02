from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

GELD_ERROR = "Please enter a a valid amount of money! (Must be a number und have a maximum amount of 2 decimal places: e.g 12.99 Euro) "
LOCATION_ERROR = "Please enter a valid location! (Must be an actual place in the format: street + number)"
TIME_ERROR = "Please enter a valid time! (Must be in the format DD.MM.YYYY HH:MM and can't be in the past)"
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
    von = StringField(
        'from',
        validators= [location_validator],
        render_kw={"placeholder": "e.g 'Lübecker Straße'"}
    )
    nach = StringField(
        'to',
        validators= [location_validator],
        render_kw={"placeholder": "e.g. 'Hauptbahnhof'"}
    )
    zeit_start = StringField(
        'gewünschte Zeit',
        validators= [zeit_validator],
        render_kw={"placeholder": "e.g '12.03.2022 08:00'"}
    )
    zeit_ende = StringField(
        'bis (optional)',
        validators= [zeit_validator],
        render_kw={"placeholder": "e.g '12.03.2022 09:00'"}
    )
    geld = StringField(
        'Kilometerpreis',
        validators = [geld_validator],
        render_kw={"placeholder": "e.g '0.99'"}
    )
    dauer = StringField(
        'Dauer in Tagen',
         validators= [dauer_validator],
         render_kw={"placeholder": "e.g '2'"}
    )
    submit = SubmitField('Create Offer')
