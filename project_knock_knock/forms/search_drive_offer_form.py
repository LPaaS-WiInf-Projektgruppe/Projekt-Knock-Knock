from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp


location_reg_ex = "^[A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df\s]*([A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df]){1}\s[0-9]{0,3}(,\s?[A-z\u00e4\u00c4\u00d6\u00f6\u00dc\u00fc\u00df]+){1}$"


class SearchDriveOfferForm(FlaskForm):
    von = StringField(
        'from',
        validators=[
            Regexp(location_reg_ex, 0, "Not a valid adress")
        ],
        render_kw={"placeholder": "e.g 'Lübecker Straße 18, Hamburg'"}
    )
    nach = StringField(
        'to',
        validators=[
            Regexp(location_reg_ex, 0, "Not a valid adress")
        ],
        render_kw={"placeholder": "e.g 'Kieler Straße 5, Hamburg'"}
    )

    submit = SubmitField("Search")
