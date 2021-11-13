from flask_user import UserMixin

from sqlalchemy import Column, Integer, String, Boolean

from extensions import db, Base


class Settings(db.Model):
    id = Column(Integer, primary_key=True)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
