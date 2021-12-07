
from flask import Flask, render_template, Blueprint


about = Blueprint('com_offer_detail', __name__)


@about.route('/com_offer_detail')
def about_func():
    return render_template('com_offer_detail.html', view_name ='Details')
