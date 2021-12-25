from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp


class SearchDriveOfferForm(FlaskForm):
    von = StringField(
        '<setting_name>',
        validators=[
            Regexp('[A-z]*', 0, "Not a valid adress")
        ],
        render_kw={"placeholder": "e.g 'Lübecker Straße'"}
    )
    nach = StringField(
        '<setting_name>',
        validators=[
            Regexp('$[A-z]*^', 0, "Not a valid adress")
        ],
        render_kw={"placeholder": "e.g 'Hauptbahnhof'"}
    )

    submit = SubmitField("Search")
