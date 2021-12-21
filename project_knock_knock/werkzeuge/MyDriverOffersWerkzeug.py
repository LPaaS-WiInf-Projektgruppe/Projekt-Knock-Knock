
from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint, redirect

from Models import User, DriverOffers
from extensions import db

from Fachwerte.work_time import WorkTime
from materialien.drive_offer import DriveOffer



my_offers = Blueprint('my_offers', __name__)

delete_driver_offer = Blueprint("delete_driver_offer", __name__)



@my_offers.route('/my_offers')
@login_required
def my_offers_func():

    # TODO: handle querying when there are no ratings or drive offers
    # TODO: add querying for ratings
    results = db.session.query(User, DriverOffers) \
        .join(DriverOffers.creator) \
        .filter_by(username = current_user.username) \
        .all()

    drive_offers = []
    for _, offer in results:
        drive_offer = DriveOffer(
            offer.id,
            offer.location,
            offer.vehicle,
            offer.created_at,
            offer.start_time,
            offer.valid_until,
            offer.kilometerpreis,
            offer.radius,
            # TODO: add actual text
            "driver_offer.text",
            # TODO: add actual rating
            3,
            offer.accepted_by

        )
        drive_offers.append(drive_offer)

    return render_template("my_drive_offers.html", view_name='My Offers', offers = drive_offers)


@my_offers.route("/delete_driver_offer/<int:offer_id>")
@login_required
def delete_driver_offer_func(offer_id):
    results = db.session.query(User, DriverOffers) \
        .join(DriverOffers.creator) \
        .filter_by(username = current_user.username) \
        .all()

    for _, offer in results:
        if offer_id == offer.id:

            offer_to_delete = DriverOffers.query.get_or_404(offer.id)
            print(offer_to_delete)
            db.session.delete(offer_to_delete)
            db.session.commit()
    return redirect('/my_offers')

    # offer_to_delete = DriverOffers.query.get_or_404(id)
    # db.session.delete(offer_to_delete)
    # db.session.commit()
