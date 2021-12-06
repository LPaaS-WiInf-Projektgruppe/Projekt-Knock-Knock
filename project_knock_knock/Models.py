from flask_user import UserMixin

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql import func

from extensions import db


message_identifier =  db.Table(
    "message_identifier",
    db.Column("nachrichten_id", db.Integer, db.ForeignKey("messages.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)

received_message_identifier =  db.Table(
    "received_message_identifier",
    db.Column("received_message_id", db.Integer, db.ForeignKey("received_messages.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)

driver_offer_identifier =  db.Table(
    "driver_offer_identifier",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("driver_offer_id", db.Integer, db.ForeignKey("driver_offers.id"))
)

driver_offer_accepted_identifier =  db.Table(
    "driver_offer_accepted_identifier",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("driver_offer_id", db.Integer, db.ForeignKey("driver_offers.id"))
)

driver_working_time_identifier =  db.Table(
    "driver_working_time_identifier",
    db.Column("working_time_id", db.Integer, db.ForeignKey("working_times.id")),
    db.Column("driver_offer_id", db.Integer, db.ForeignKey("driver_offers.id"))
)

com_offer_identifier =  db.Table(
    "com_offer_identifier",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("com_offer_id", db.Integer, db.ForeignKey("com_offers.id"))
)

com_offer_accepted_identifier =  db.Table(
    "com_offer_accepted_identifier",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("com_offer_id", db.Integer, db.ForeignKey("com_offers.id"))
)

workingtime_identifier = db.Table(
    "workingtime_identifier",
    db.Column("working_times", db.Integer, db.ForeignKey("working_times.id")),
    db.Column("weekdays", db.Integer, db.ForeignKey("weekdays.id"))
)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    messages = db.relationship("Message", secondary= message_identifier)
    received_messages = db.relationship("ReceivedMessage", secondary= received_message_identifier)
    com_offers = db.relationship("ComOffers", secondary= com_offer_identifier)
    driver_offers = db.relationship("DriverOffers", secondary= driver_offer_identifier)


class Rating(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable = True)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key= True)
    created_at = db.Column(db.DateTime, nullable = False)
    text = db.Column(db.String(500), nullable = False)

class ReceivedMessage(db.Model):
    __tablename__ = "received_messages"
    id = db.Column(db.Integer, primary_key= True)
    created_at = db.Column(db.DateTime, nullable = False)
    text = db.Column(db.String(500), nullable = False)

class WorkingTime(db.Model):
    __tablename__ = "working_times"
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer, nullable = True)

    weekdays = db.relationship("Weekday", secondary= workingtime_identifier)

class Weekday(db.Model):
    __tablename__ = "weekdays"
    id = db.Column(db.Integer, primary_key = True)
    weekday = db.Column(db.String(50), nullable = False)




# # Entwurf Datenbank-Table für die Angebote
# class Offers(db.Model):
#     __tablename__ = ""
#     id = db.Column(db.Integer, primary_key=True)
#     start = db.Column(db.String(50), nullable=False)
#     end = db.Column(db.String(50), nullable=False)
#     time = db.Column(db.DateTime, nullable=True)
#     money = db.Column(db.Integer(), nullable=False)

# Datenbank-Table für die Angebote der Unternehmen
class ComOffers(db.Model):
    __tablename__ = "com_offers"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable = True)
    kilometerpreis = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())


# Datenbank-Table für die Angebote der Fahrer
class DriverOffers(db.Model):
    __tablename__ = "driver_offers"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    vehicle = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, default= "NULL")
    kilometerpreis = db.Column(db.Integer, nullable=False, default = 0)
    radius = db.Column(db.Integer, nullable = True)
    text = db.Column(db.String(140), nullable = True)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.id'))

    rating = db.relationship("Rating")
    working_time = db.relationship(
        "WorkingTime",
        secondary = driver_working_time_identifier
    )
