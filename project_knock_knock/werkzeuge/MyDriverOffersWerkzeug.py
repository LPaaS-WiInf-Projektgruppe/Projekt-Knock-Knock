
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
    results = db.session.query(User, DriverOffers) \
        .join(DriverOffers.creator) \
        .filter_by(username = current_user.username) \
        .all()




    print(results)


    drive_offers = []
    for _, offer in results:
        # work_time = WorkingTime(
        #     driver_offer.weekday,
        #     driver_offer.start_time,
        #     driver_offer.end_time
        # )

        # print(driver_offer.vehicle)



        drive_offer = DriveOffer(
            offer.location,
            offer.vehicle,
            offer.created_at,
            offer.start_time,
            offer.end_time,
            offer.kilometerpreis,
            offer.radius,
            # TODO: add actual text
            "driver_offer.text",
            # TODO: add actual rating
            3
        )
        drive_offers.append(drive_offer)
    print(drive_offers)



    return render_template("my_drive_offers.html", view_name='My Offers', offers = drive_offers)
