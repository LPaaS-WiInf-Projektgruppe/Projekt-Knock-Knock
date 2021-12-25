
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
    user_accepted_drive_offers_query = db.session.query(User, DriverOffers) \
        .filter(User.id == DriverOffers.accepted_by) \
        .filter(DriverOffers.completed_at == None) \
        .filter_by(username = curr_user) \
        .all()

    # query database for every company offer that the user accepted
    user_accepted_com_offers_query = db.session.query(User, ComOffers) \
        .filter(User.id == ComOffers.accepted_by) \
        .filter(ComOffers.completed_at == None) \
        .filter_by(username = curr_user) \
        .all()

    # print("accepted drive offers: {} \n" \
    #     "accepted company offers:"
    #     .format(user_accepted_drive_offers))

    user_accepted_drive_offers = []
    for _, drive_offer in user_accepted_drive_offers_query:
        user_accepted_drive_offer = DriveOffer(
            drive_offer.id,
            drive_offer.location,
            drive_offer.vehicle,
            drive_offer.created_at,
            drive_offer.creator,
            drive_offer.start_time,
            drive_offer.valid_until,
            drive_offer.kilometerpreis,
            drive_offer.radius,
            drive_offer.text,
            "NULL",
            drive_offer.accepted_by
        )
        user_accepted_drive_offers.append(user_accepted_drive_offer)


    user_accepted_com_offers = []
    for _, com_offer in user_accepted_com_offers_query:
        user_accepted_com_offer = ComOffer(
            com_offer.id,
            com_offer.start,
            com_offer.destination,
            com_offer.start_time,
            com_offer.end_time,
            com_offer.kilometerpreis,
            com_offer.created_at,
            com_offer.creator,
            0
        )
        user_accepted_com_offers.append(user_accepted_com_offer)

    work_times = []
    for user, work_time in result:
        work_time = wt(
            work_time.weekday,
            work_time.start_time,
            work_time.end_time
        )
        work_times.append(work_time)

    # get the rating for a user from the database
    drive_offer_rating = db.session.query(Rating) \
        .select_from(Rating) \
        .join(DriverOffers, Rating.drive_offer) \
        .join(User, DriverOffers.creator) \
        .filter(User.username == curr_user) \
        .all()


    com_offer_rating = db.session.query(Rating) \
        .select_from(Rating) \
        .join(ComOffers, Rating.com_offer) \
        .join(User, ComOffers.creator) \
        .filter(User.username == curr_user) \
        .all()

    ratings = []
    for r in drive_offer_rating:
        ratings.append(r.stars)
    for r in com_offer_rating:
        ratings.append(r.stars)

    rating = fw_rating(ratings)

    try:
        # TODO: add a description, currently uses username as default
        user_profile = Profil(
            result[0][0].username,
            work_times,
            user_accepted_drive_offers,
            user_accepted_com_offers,
            rating,
            result[0][0].username
        )

    except IndexError:
        # handle case where the are no working_times saved for the user
        result = User.query.filter_by(username = current_user.username).first()
        user_profile = Profil(
            result.username,
            [],
            user_accepted_drive_offers,
            user_accepted_com_offers,
            rating,
            ""
        )

    return render_template("profil.html", view_name='Profil', profile = user_profile)
