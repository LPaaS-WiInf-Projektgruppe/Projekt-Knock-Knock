from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeField, FloatField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

GELD_ERROR = "Please enter a a valid amount of money! (Must be a number und have a maximum amount of 2 decimal places: e.g 12.99 Euro) "
LOCATION_ERROR = "Please enter a valid location! (Must be an actual place in the format: street + number)"
FAHRZEUG_ERROR = "Please enter a valid vehicle! (Must be an actual vehicle e.g. Mercedes Sprinter)"
TIME_ERROR = "Please enter a valid time! (Must be in the format DD.MM.YYYY HH:MM and can't be in the past)"
UMKREIS_ERROR = "Must be a valid range! (Must be a number between 0 and 99) "
BEMERKUNGEN_ERROR = "Please enter a valid input! (Must be below 100 characters!)"
UHRZEIT_ERROR = "Please enter a valid time! (Must be in the format HH:MM)"

location_validator = Regexp("^[A-z]+\s?[0-9]{0,3}$", 0, message = LOCATION_ERROR)

fahrzeug_validator = Regexp("^[A-z]+\s?[0-9]{0,4}[A-z]*\s?[0-9]{0,4}$", 0, message = FAHRZEUG_ERROR)

geld_validator = Regexp("^[0-9]*\.[0-9][0-9]$", 0, message = GELD_ERROR)

zeit_validator = Regexp("^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9]\s[0-9][0-9]\:[0-9][0-9]$", 0, message = TIME_ERROR)

uhrzeit_validator = Regexp("^[0-9][0-9]\:[0-9][0-9]$", 0, message = UHRZEIT_ERROR)

umkreis_validator = Regexp("^[0-9]{1,2}$", 0, message = UMKREIS_ERROR)

bemerkungen_validator = Regexp("^[A-z]{0,100}$", 0, message = BEMERKUNGEN_ERROR)

class DriverOfferForm(FlaskForm):
    ort = StringField('Ort:', validators= [location_validator])
    fahrzeug = StringField('Fahrzeug:', validators= [fahrzeug_validator])
    zeit_start = StringField('Verfügbar ab:', validators= [zeit_validator])
    zeit_ende = StringField('Verfügbar bis:', validators= [zeit_validator])
    from_zeitMo = StringField('Montag:', validators= [uhrzeit_validator])
    from_zeitDi = StringField('Dienstag:', validators= [uhrzeit_validator])
    from_zeitMi = StringField('Mittwoch:', validators= [uhrzeit_validator])
    from_zeitDo = StringField('Donnerstag:', validators= [uhrzeit_validator])
    from_zeitFr = StringField('Freitag:', validators= [uhrzeit_validator])
    from_zeitSa = StringField('Samstag:', validators= [uhrzeit_validator])
    from_zeitSo = StringField('Sonntag:', validators= [uhrzeit_validator])
    # to_zeitMo = StringField('Montag:', validators= [uhrzeit_validator])
    # to_zeitDi = StringField('Dienstag:', validators= [uhrzeit_validator])
    # to_zeitMi = StringField('Mittwoch:', validators= [uhrzeit_validator])
    # to_zeitDo = StringField('Donnerstag:', validators= [uhrzeit_validator])
    # to_zeitFr = StringField('Freitag:', validators= [uhrzeit_validator])
    # to_zeitSa = StringField('Samstag:', validators= [uhrzeit_validator])
    # to_zeitSo = StringField('Sonntag:', validators= [uhrzeit_validator])
    preis = StringField('Kilometerpreis:', validators = [geld_validator])
    radius = StringField('Umkreis in km:', validators = [umkreis_validator])
    bemerkungen = StringField('Bemerkungen:', validators = [bemerkungen_validator])
    submit = SubmitField('Create Offer')
