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
from werkzeuge.DriverOfferDetailWerkzeug import driver_offer_detail
from werkzeuge.ProfilWerkzeug import profil
from werkzeuge.MyDriverOffersWerkzeug import my_offers
from werkzeuge.MyComOffersWerkzeug import my_orders
from werkzeuge.ChatWerkzeug import chat
from werkzeuge.ConversationsWerkzeug import conversations
from werkzeuge.RateOfferWerkzeug import rate_offer
from werkzeuge.MapWerkzeug import map


from Models import User
from extensions import db
from startup import initialCode, todo

def createApp(config_file= 'config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    user_manager = UserManager(app, db, User)

    fa = FontAwesome(app)

    app.register_blueprint(initialCode)
    app.register_blueprint(todo)
    app.register_blueprint(home)
    app.register_blueprint(index)
    app.register_blueprint(settings)
    app.register_blueprint(about)
    app.register_blueprint(comOffer)
    app.register_blueprint(my_orders)
    app.register_blueprint(com_offer_detail)
    app.register_blueprint(driver_offer_detail)
    app.register_blueprint(driverOffer)
    app.register_blueprint(my_offers)
    app.register_blueprint(profil)
    app.register_blueprint(chat)
    app.register_blueprint(conversations)
    app.register_blueprint(rate_offer)
    app.register_blueprint(map)



    db.init_app(app)

    return app
