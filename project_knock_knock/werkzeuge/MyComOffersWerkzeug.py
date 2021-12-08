
from flask_user import login_required, current_user
from flask import Flask, render_template, Blueprint

from Models import User, ComOffers

from extensions import db



my_orders = Blueprint('my_orders', __name__)


@my_orders.route('/my_orders')
@login_required
def redirect_home():

    return render_template("my_orders.html", view_name='My Orders')
