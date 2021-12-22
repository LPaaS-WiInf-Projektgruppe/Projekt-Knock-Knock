
from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint

from Models import User, ComOffers
from extensions import db

from materialien.com_offer import ComOffer



my_orders = Blueprint('my_orders', __name__)


@my_orders.route('/my_orders')
@login_required
def my_orders_func():

    # TODO: handle querying when there are no ratings or com offers
    # TODO: add querying for ratings
    results = db.session.query(User, ComOffers) \
        .join(ComOffers.creator) \
        .filter_by(username = current_user.username) \
        .all()

    # print(results)


    com_offers = []
    for _, offer in results:

        com_offer = ComOffer(
            offer.id,
            offer.start,
            offer.destination,
            offer.start_time,
            offer.end_time,
            offer.kilometerpreis,
            offer.created_at,
            offer.creator,
            # TODO: add actual text
            # TODO: add actual rating
            3
        )
        com_offers.append(com_offer)
    print(com_offers)



    return render_template("my_com_offers.html", view_name='My Orders', offers = com_offers)
