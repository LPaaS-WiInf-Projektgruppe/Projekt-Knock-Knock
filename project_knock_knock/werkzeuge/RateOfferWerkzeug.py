
from flask import Flask, render_template, Blueprint, request, redirect
from flask_user import login_required
from forms.rating_offer_form import RatingForm

from Models import DriverOffers, ComOffers, Rating
from forms.settings_form import SettingsForm
from materialien.Database import SQLDatabase
from extensions import db

rate_offer = Blueprint('rate_offer', __name__)



@rate_offer.route("/rate_offer/<int:type>/<int:offer_id>", methods= ['GET', 'POST'])
# @login_required
def rate_offer_func(type, offer_id):
    form = RatingForm()

    if form.validate_on_submit():
        form_rating = form.rating.data

        # add rating to the offer depending on its type
        if type == 0:
            rating = Rating(
                stars = form_rating,
                drive_offer_id = offer_id
            )
            db.session.add(rating)

            db.session.add(rating)
        else:
            rating = Rating(
                stars = form_rating,
                drive_offer_id = offer_id
            )
            db.session.add(rating)


        db.session.commit()
        return redirect("/home")

    else:
        return render_template(
            "rate_offer.html",
            form = form,
            type = type,
            id = offer_id,
            view_name= "Rate the Offer"
            )
