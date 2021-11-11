
from flask_user import login_required
from flask import Flask, render_template, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


home = Blueprint('home', __name__)
index = Blueprint('index', __name__)

# uri = URI(DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD)
# uri = uri.get_uri_string()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)

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
        refill_time = refill_time)
