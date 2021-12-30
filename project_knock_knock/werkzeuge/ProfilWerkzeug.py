
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

    user_accepted_com_offers = ComOffers.get_user_accepted_offers(current_user)
    user_created_com_offers = ComOffers.get_user_created_offers(current_user)
    user_accepted_drive_offers = DriverOffers.get_user_accepted_offers(current_user)
    user_created_drive_offers = DriverOffers.get_user_created_offers(current_user)
    rating = Rating.get_user_rating(current_user)
    work_times = WorkingTime.get_worktime_for_user(current_user)

    for item in user_created_drive_offers:
        print("user_created_drive_offers: {}".format(item.is_accepted()))

    try:
        # TODO: add a description, currently uses username as default
        user_profile = Profil(
            current_user.username,
            rating,
            user_created_drive_offers,
            user_created_com_offers,
            work_times,
            user_accepted_drive_offers,
            user_accepted_com_offers,
            "description"
        )

    except IndexError:
        # handle case where the are no working_times saved for the user
        result = User.query.filter_by(username = current_user.username).first()
        user_profile = Profil(
            current_user.username,
            rating,
            user_created_drive_offers,
            user_created_com_offers,
            [],
            user_accepted_drive_offers,
            user_accepted_com_offers,
            "description"
        )

    return render_template("profil.html", view_name='Profil', profile = user_profile)
