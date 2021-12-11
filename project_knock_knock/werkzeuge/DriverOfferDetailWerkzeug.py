
from flask import Flask, render_template, Blueprint
from flask_user import current_user, login_required
from Models import DriverOffers


driver_offer_detail = Blueprint('driver_offer_detail', __name__)


@driver_offer_detail.route('/driver_offer_detail/<int:offer_id>')
@login_required
def driver_offer_detail_func(offer_id):

    driver_offer = DriverOffers.query.filter_by(id = offer_id).first()

    return render_template('driver_offer_detail.html', view_name ='Details', data = driver_offer)
