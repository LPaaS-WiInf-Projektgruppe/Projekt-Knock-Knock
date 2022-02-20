
from flask_user import login_required
from flask_user.forms import RegisterForm
from flask import Flask, render_template, Blueprint
# from forms.register_form import RegisterForm



home = Blueprint('home', __name__)
index = Blueprint('index', __name__)


@index.route('/', methods=["GET", "POST"])
# @login_required
def redirect_home():

    form = RegisterForm()

    return render_template("home.html", view_name='Home', form = form)



@home.route('/home', methods=["GET", "POST"])
# @login_required
def home_func():

    form = RegisterForm()

    return render_template(
        "home.html",
        view_name='Home',
        form = form
        )
