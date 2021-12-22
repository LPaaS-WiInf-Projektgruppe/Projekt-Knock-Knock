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



initialCode = Blueprint('initialCode', __name__)
todo = Blueprint('todo', __name__)



@initialCode.before_app_first_request
def def_initial_code():
    """initialize services that are requiered at startup """

    db.create_all()

    #Initialer "User"-Eintrag für den Support Zugang
    #supportUser = User(id = 99999, username="Support", password="Test2020")
    #try:
    #    db.session.add(supportUser)
    #    db.session.commit()
    #except:
    #    pass

@todo.route("/todo")
def todo_func():
    """return todo page"""

    return "This functionality is unfortunatly not supported yet. Try again later"
