from flask import Flask, Blueprint
from flask_fontawesome import FontAwesome
from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy


from werkzeuge.HomeWerkzeug import  home, index
from werkzeuge.SettingsWerkzeug import settings
from werkzeuge.AboutWerkzeug import about
from werkzeuge.ComOfferWerkzeug import comOffer
from werkzeuge.DriverOfferWerkzeug import driverOffer
from werkzeuge.ComOfferDetailWerkzeug import com_offer_detail

from Models import User
from extensions import db
from startup import initialCode

def createApp(config_file= 'config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    user_manager = UserManager(app, db, User)

    fa = FontAwesome(app)

    app.register_blueprint(initialCode)

    app.register_blueprint(home)
    app.register_blueprint(index)
    app.register_blueprint(settings)
    app.register_blueprint(about)
    app.register_blueprint(comOffer)
    app.register_blueprint(com_offer_detail)
    app.register_blueprint(driverOffer)


    db.init_app(app)

    return app
