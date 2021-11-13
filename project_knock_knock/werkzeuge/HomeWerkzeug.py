
from flask_user import login_required
from flask import Flask, render_template, Blueprint



home = Blueprint('home', __name__)
index = Blueprint('index', __name__)


@index.route('/')
@login_required
def redirect_home():
    return render_template("home.html", view_name='Home')



@home.route('/home')
@login_required
def home_func():

    return render_template(
        "home.html",
        view_name='Home',
        )
