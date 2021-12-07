
from flask import Flask, render_template, Blueprint
from flask_user import current_user, login_required
from Models import ComOffers, User



com_offer_detail = Blueprint('com_offer_detail', __name__)


@com_offer_detail.route('/com_offer_detail/<int:offer_id>')
@login_required
def com_offer_detail_func(offer_id):

    com_offer = ComOffers.query.filter_by(id = offer_id).first()

    print(com_offer.start)

    return render_template('com_offer_detail.html', view_name ='Details', data = com_offer)
