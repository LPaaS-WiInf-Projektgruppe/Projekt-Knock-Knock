import json

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask_user import login_required
from flask import Flask, render_template, Blueprint

from config import DB_NAME, SQLALCHEMY_DATABASE_URI
# from Models import Settings
from extensions import db
from materialien.Database import SQLDatabase
from Models import User
from flask_user import UserManager
from Models import User
from flask import current_app



initialCode = Blueprint('initialCode', __name__)
todo = Blueprint('todo', __name__)



@initialCode.before_app_first_request
def def_initial_code():
    """initialize services that are requiered at startup """

    db.create_all()

    user_manager = current_app.user_manager
    password_hash = user_manager.hash_password("Test2020")
    support_exists = db.session.query(User).filter_by(username = "Support3").first()

    if not support_exists:
        supportUser = User(username="Support3", password =password_hash, active = 1)
        try:
            db.session.add(supportUser)
            db.session.commit()
        except:
            return "Fehler beim Anlegen des Support-Zugang!"

    #Sollte das funktionieren, benötigt man lediglich folgenden Inhalt in HTML
    #um mit dem Support chatten zu können:
    #<div class="btn" onclick="location.href='/chat/IDdesSUPPORT'">
    #Contact Support
    #</div>


@todo.route("/todo")
def todo_func():
    """return todo page"""

    return "This functionality is unfortunatly not supported yet. Try again later"
