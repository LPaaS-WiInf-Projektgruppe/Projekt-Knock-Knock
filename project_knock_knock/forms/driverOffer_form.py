from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, FloatField, SelectField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField, TimeField, TelField

from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp

GELD_ERROR = "Please enter a a valid amount of money! (Must be a number und have a maximum amount of 2 decimal places: e.g 12.99 Euro) "
LOCATION_ERROR = "Please enter a valid location! (Must be an actual place in the format: street + number)"
FAHRZEUG_ERROR = "Please enter a valid vehicle! (Must be an actual vehicle e.g. Mercedes Sprinter)"
TIME_ERROR = "Please enter a valid time! (Must be in the format DD.MM.YYYY HH:MM and can't be in the past)"
UMKREIS_ERROR = "Must be a valid range! (Must be a number between 0 and 99) "
BEMERKUNGEN_ERROR = "Please enter a valid input! (Must be below 100 characters!)"
UHRZEIT_ERROR = "Please enter a valid time! (Must be in the format HH:MM)"

location_reg_ex = "^[A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df\s]*([A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df]){1}\s[0-9]{0,3}(,\s?[A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df]+){1}$"
fahrzeug_reg_ex = "^[A-z]+\s?[0-9]{0,4}[A-z]*\s?[0-9]{0,4}$"
geld_reg_ex = "^[0-9]*\.[0-9][0-9]$"
zeit_reg_ex = "^[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9]\s[0-9][0-9]\:[0-9][0-9]$"
uhrzeit_reg_ex = "^[0-9][0-9]\:[0-9][0-9]$"
radius_reg_ex = "^[0-9]{1,2}$"
bemerkungen_reg_ex = "^[A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df\s!\?\.:]{0,100}$"

location_validator = Regexp(location_reg_ex, 0, message = LOCATION_ERROR)

fahrzeug_validator = Regexp(fahrzeug_reg_ex, 0, message = FAHRZEUG_ERROR)

geld_validator = Regexp(geld_reg_ex, 0, message = GELD_ERROR)

zeit_validator = Regexp(zeit_reg_ex, 0, message = TIME_ERROR)

uhrzeit_validator = Regexp(uhrzeit_reg_ex, 0, message = UHRZEIT_ERROR)

umkreis_validator = Regexp(radius_reg_ex, 0, message = UMKREIS_ERROR)

bemerkungen_validator = Regexp(bemerkungen_reg_ex, 0, message = BEMERKUNGEN_ERROR)

select_choices = {25:"25 km", 50:"50 km", 100:"100 km", 200:"200 km"}

class DriverOfferForm(FlaskForm):
    ort = StringField('Location:', validators= [location_validator], render_kw={"placeholder": "e.g 'Lübecker Straße 18, Hamburg'"})
    fahrzeug = StringField('Vehicle:', validators= [fahrzeug_validator], render_kw={"placeholder": "e.g 'Hyundai i20'"})
    zeit_start = DateTimeLocalField('Available from:', format="%Y-%m-%dT%H:%M", render_kw={"placeholder": "e.g '12.21.2022 08:00'"})
    zeit_ende = DateTimeLocalField('Available until:', format="%Y-%m-%dT%H:%M", validators= [], render_kw={"placeholder": "e.g '13.21.2022 16:00'"})
    from_zeitMo = TimeField('Monday:', validators= [], format="%H:%M", render_kw={"placeholder": "08:00"})
    from_zeitDi = TimeField('Tuesday:', validators= [], format="%H:%M", render_kw={"placeholder": "08:00"})
    from_zeitMi = TimeField('Wednesday:', validators= [], format="%H:%M", render_kw={"placeholder": "08:00"})
    from_zeitDo = TimeField('Thursday:', validators= [], format="%H:%M", render_kw={"placeholder": "'08:00"})
    from_zeitFr = TimeField('Friday:', validators= [], format="%H:%M", render_kw={"placeholder": "08:00"})
    from_zeitSa = TimeField('Saturday:', validators= [], format="%H:%M", render_kw={"placeholder": "08:00"})
    from_zeitSo = TimeField('Sunday:', validators= [], format="%H:%M", render_kw={"placeholder": "'08:00"})
    to_zeitMo = TimeField('Monday:', validators= [], format="%H:%M", render_kw={"placeholder": "16:00"})
    to_zeitDi = TimeField('Tuesday:', validators= [], format="%H:%M", render_kw={"placeholder": "16:00"})
    to_zeitMi = TimeField('Wednesday:', validators= [], format="%H:%M", render_kw={"placeholder": "16:00"})
    to_zeitDo = TimeField('Thursday:', validators= [], format="%H:%M", render_kw={"placeholder": "16:00"})
    to_zeitFr = TimeField('Friday:', validators= [], format="%H:%M", render_kw={"placeholder": "16:00"})
    to_zeitSa = TimeField('Saturday:', validators= [], format="%H:%M", render_kw={"placeholder": "16:00'"})
    to_zeitSo = TimeField('Sunday:', validators= [], format="%H:%M", render_kw={"placeholder": "16:00"})
    preis = TelField('Price per kilometer:', validators = [geld_validator],render_kw={"placeholder": "e.g '0.99'"})
    radius = SelectField('Range in km:', choices = select_choices, coerce=str)
    bemerkungen = TextAreaField('Additional notifications:', validators = [bemerkungen_validator], render_kw={"placeholder": "e.g 'No Smoking!'"})
    submit = SubmitField('Create Offer', render_kw={"val": "e.g 'No Smoking!'"})
