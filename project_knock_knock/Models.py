from flask_user import UserMixin

from sqlalchemy import Column, Integer, String, Boolean

from extensions import db


class Settings(db.Model):
    id = Column(Integer, primary_key=True)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)


# Datenbank-Table für die Angebote
class Offers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(50), nullable=False)
    end = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, nullable=True)
    money = db.Column(db.Integer(), nullable=False)

# Datenbank-Table für die Angebote der Unternehmen
class comOffers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(50), nullable=False)
    end = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, nullable=True)
    money = db.Column(db.Integer(), nullable=False)
