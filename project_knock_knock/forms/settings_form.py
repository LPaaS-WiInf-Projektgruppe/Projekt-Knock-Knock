from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp


class SettingsForm(FlaskForm):
    location = StringField(
        '<setting_name>',
        validators=[
            Regexp('<reg ex>', 0, "<error_message>")
        ]
    )
