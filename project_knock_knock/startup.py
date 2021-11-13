import json

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask_user import login_required
from flask import Flask, render_template, Blueprint

from config import DB_NAME, SQLALCHEMY_DATABASE_URI
from Models import Settings
from extensions import db
from materialien.Database import SQLDatabase



initialCode = Blueprint('initialCode', __name__)



@initialCode.before_app_first_request
def activate_job():
    """initialize database tables (create and add an entry)
    if they are not yet initialized (first start)
    initilize state of the system when restarting """

    sql_db = SQLDatabase(uri)
    sql_db.add_database()

    db.create_all()


    # CREATE INITIAL TABLE ENTRIES FOR SETTINGS
    settings = Settings(
        id=1,
    )


    with session as sess:
        # ADD NEW TABLE ENTRY IF NONE EXIST YET
        if sess.query(Settings).first() == None:
            sess.add(settings)
        sess.commit()
