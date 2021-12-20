
from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint

from extensions import db
from Models import WorkingTime, User, DriverOffers, ComOffers, Rating
from Fachwerte.work_time import WorkTime as wt
from Fachwerte.rating import Rating as fw_rating
from materialien.profil import Profil
from materialien.drive_offer import DriveOffer
from materialien.com_offer import ComOffer



profil = Blueprint('profil', __name__)



@profil.route('/profil')
@login_required
def profil_func():
    curr_user = current_user.username
    # query database for every entry that belongs to the user and
    # returns the work time
    result = db.session.query(User, WorkingTime) \
        .join(WorkingTime.user) \
        .filter_by(username = curr_user) \
        .order_by(WorkingTime.weekday) \
        .all()

    # query database for every drive offer that the user accepted
    user_accepted_drive_offers = db.session.query(User, DriverOffers) \
        .filter(User.id == DriverOffers.accepted_by) \
        .filter_by(username = curr_user).all()

    # query database for every company offer that the user accepted
    # user_accepted_com_offers = db.session.query(User, ComOffers, Rating) \
    #     .filter(User.id == DriverOffers.accepted_by) \
    #     .filter(Rating.drive_offer_id == DriverOffers.id) \
    #     .filter_by(username = curr_user).all()

    print("accepted drive offers: {} \n" \
        "accepted company offers:"
        .format(user_accepted_drive_offers))

    drive_offers = []
    for _, drive_offer in user_accepted_drive_offers:
        offer = DriveOffer(
            drive_offer.id,
            drive_offer.location,
            drive_offer.vehicle,
            drive_offer.created_at,
            drive_offer.start_time,
            drive_offer.end_time,
            drive_offer.kilometerpreis,
            drive_offer.radius,
            drive_offer.text,
            "NULL",
            drive_offer.accepted_by
        )
        drive_offers.append(offer)

    work_times = []
    for user, work_time in result:
        work_time = wt(
            work_time.weekday,
            work_time.start_time,
            work_time.end_time
        )
        work_times.append(work_time)

    # get the rating for a user from the database
    rating_results = db.session.query(User, DriverOffers, Rating) \
        .filter(DriverOffers.id == Rating.drive_offer) \
        .filter_by(username = curr_user) \
        .all()

    ratings = []
    for _, _ , r in rating_results:
        ratings.append(r.stars)

    rating = fw_rating(ratings)

    try:
        # TODO: add a description, currently uses username as default
        user_profile = Profil(
            result[0][0].username,
            work_times,
            drive_offers,
            rating,
            result[0][0].username
        )

    except IndexError:
        # handle case where the are no working_ times saved for the user
        result = User.query.filter_by(username = current_user.username).first()
        user_profile = Profil(result.username, [], drive_offers,  0, "")

    return render_template("profil.html", view_name='Profil', profile = user_profile)
