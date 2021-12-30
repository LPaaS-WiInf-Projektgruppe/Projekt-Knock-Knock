
from flask import Flask, render_template, Blueprint, request, redirect
from flask_user import login_required
from forms.rating_offer_form import RatingForm

from datetime import datetime

from Models import DriverOffers, ComOffers, Rating
from forms.settings_form import SettingsForm
from materialien.Database import SQLDatabase
from extensions import db

rate_offer = Blueprint('rate_offer', __name__)



@rate_offer.route("/rate_offer/<int:type>/<int:offer_id>", methods= ['GET', 'POST'])
@login_required
def rate_offer_func(type, offer_id):
    form = RatingForm()

    if form.validate_on_submit():
        form_rating = form.rating.data
        Rating.rate_offer(offer_id, type, form_rating)

        return redirect("/profil")

    else:
        return render_template(
            "rate_offer.html",
            form = form,
            type = type,
            id = offer_id,
            view_name= "Rate the Offer"
            )
