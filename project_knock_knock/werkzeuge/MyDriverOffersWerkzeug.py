
from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint

from Models import User, DriverOffers
from extensions import db

from Fachwerte.work_time import WorkTime
from materialien.drive_offer import DriveOffer



my_offers = Blueprint('my_offers', __name__)



@my_offers.route('/my_offers')
@login_required
def my_offers_func():

    # TODO: handle querying when there are no ratings or drive offers
    # TODO: add querying for ratings
    offers = db.session.query(User, DriverOffers) \
        .join(DriverOffers.creator) \
        .filter_by(username = current_user.username) \
        .all()



    for _, driver_offer in offers:
        work_time = WorkingTime(
            driver_offers.weekday,
            driver_offers.start_time,
            driver_offers.end_time
        )

        offer = DriveOffer(
            driver_offer.location,
            driver_offer.vehicle,
            driver_offer.created_at,
            driver_offer.start_time,
            driver_offer.end_time,
            driver_offer.kilometerpreis,
            driver_offer.radius,
            # TODO: add actual text
            "driver_offer.text",
            # TODO: add actual rating
            3,
        )



    return render_template("my_drive_offers.html", view_name='My Offers', offers = offers)
