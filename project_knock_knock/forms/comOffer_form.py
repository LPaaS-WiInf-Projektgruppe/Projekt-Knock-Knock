from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.fields.html5 import DateTimeLocalField, TimeField, TelField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

GELD_ERROR = "Please enter a a valid amount of money! (Must be a number und have a maximum amount of 2 decimal places: e.g 12.99 Euro) "
LOCATION_ERROR = "Please enter a valid location! (Must be an actual place in the format: street + number)"
TIME_ERROR = "Please enter a valid time! (Must be in the format DD.MM.YYYY HH:MM and can't be in the past)"
DURATION_ERROR = "Must be a valid duration! (Must be a number and have a maximum amount of 1 decimal place: e.g. 1.5. Furthermore duration has to be be larger than 0 and smaller than 7 in order to be accepted.) "

location_reg_ex = "^[A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df\s]*([A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df]){1}\s[0-9]{0,3}(,\s?[A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df]+){1}$"
location_validator = Regexp(location_reg_ex, 0, message = LOCATION_ERROR)

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
        render_kw={"placeholder": "e.g 'Lübecker Straße 5, Hamburg'"}
    )
    nach = StringField(
        'to',
        validators= [location_validator],
        render_kw={"placeholder": "e.g. 'Kieler Straße 5, Hamburg'"}
    )
    zeit_start = DateTimeLocalField(
        'gewünschte Zeit',
        format="%Y-%m-%dT%H:%M",
        render_kw={"placeholder": "e.g '12.03.2022 08:00'"}
    )
    zeit_ende = DateTimeLocalField(
        'bis (optional)',
        format="%Y-%m-%dT%H:%M",
        render_kw={"placeholder": "e.g '12.03.2022 09:00'"}
    )
    geld = TelField(
        'Kilometerpreis',
        validators = [geld_validator],
        render_kw={"placeholder": "e.g '0.99'"}
    )
    dauer = TelField(
        'Dauer in Tagen',
         validators= [dauer_validator],
         render_kw={"placeholder": "e.g '2'"}
    )
    submit = SubmitField('Create Offer')
