
from flask import Flask, render_template, Blueprint
from flask_user import login_required

from WateringApp.Models import Settings
from WateringApp.forms.settings_form import SettingsForm

from WateringApp.materialien.Database import SQLDatabase





settings = Blueprint('settings', __name__)


@settings.route("/settings", methods= ['GET', 'POST'])
@login_required
def settings_page():
    form = SettingsForm()

    if form.validate_on_submit():
        # handle form submission
        # print('form submitted')

        # example
        # if form.from_attribute.data == "string":
        #     do something


    return render_template(
        "settings.html",
        form = form,
        settings = settings
    )
