from flask_user import UserMixin

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql import func

from extensions import db





# association tables for n:m relationships between tables

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

working_time_identifier =  db.Table(
    "working_time_identifier",
    db.Column("working_time_id", db.Integer, db.ForeignKey("working_times.id")),
    db.Column("driver_offer_id", db.Integer, db.ForeignKey("users.id"))
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


# Table that represents a users
#
class User(db.Model, UserMixin):
    ''' Table that represents a users

    Columns
     :id: identifies a users
     :username: a unique name to login with
     :password: the corresponding password
    '''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(140), nullable=True)
    active = db.Column(db.Boolean(), nullable = False, server_default='0')

    accepted_drive_offer = db.relationship("DriverOffers", backref='driver_offers.accepted_by')
    accepted_com_offer = db.relationship("ComOffers", backref='com_offers.accepted_by')

    db.relationship("Message", backref="send_messages")
    db.relationship("Message", backref="rec_messages")

    messages = db.relationship(
        "Message",
        secondary= message_identifier,
        backref= db.backref("creator", lazy ="dynamic")
    )
    received_messages = db.relationship(
        "ReceivedMessage",
        secondary= received_message_identifier,
        backref= db.backref("receiver", lazy ="dynamic")
    )
    com_offers = db.relationship(
        "ComOffers",
        secondary= com_offer_identifier,
        backref= db.backref("creator", lazy ="dynamic")
    )
    driver_offers = db.relationship(
        "DriverOffers",
        secondary= driver_offer_identifier,
        backref= db.backref("creator", lazy ="dynamic")
    )

    working_time = db.relationship(
            "WorkingTime",
            secondary = working_time_identifier,
            backref = db.backref("user", lazy="dynamic")
    )


class Rating(db.Model):
    ''' Represents a the Rating of an Offer

    Columns
    :id primary_key: the unique identifier for the rating
    :stars: - the rating for an offer
    :drive_offer_id foreign_key: - the drive offer the rating belongs to
    :com_offer_id foreign_key: - the company offer the rating belongs to

    '''
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable = True)
    drive_offer_id = db.Column(db.Integer, db.ForeignKey("driver_offers.id"))
    com_offer_id = db.Column(db.Integer, db.ForeignKey("com_offers.id"))

class Message(db.Model):
    ''' Represents a Message written by a User
    '''
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key= True)
    created_at = db.Column(db.DateTime, nullable = False)
    text = db.Column(db.String(500), nullable = False)
    from_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class WorkingTime(db.Model):
    ''' Represents the Working Time of a user as a driver

    Columns
    :id primary_key: - the unique identifier for the working time entry
    :start_time: - specifies the start time for a weekday
    :end_time: - specifies the end time for a weekday
    :weekday: - the day of the week for which the start and end time is meant
    '''
    __tablename__ = "working_times"
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Integer, nullable = True)
    end_time = db.Column(db.Integer, nullable = True)
    weekday = db.Column(db.Integer, nullable= True)


class ComOffers(db.Model):
    '''Represents a Company Offer as a DB table

    Columns
    :id primary_key: - the unique identifier for the company offer
    :start: - the start location of the offer
    :destination: - the destination of the offer
    :start_time: - the date and time when the offer is starting
    :end_time: - the date and time when the offer is ending is
                 default = start_time
    :kilometerpreis: - the price the user who created the offer
                       is willing to pay per kilometer
    :created_at: the date and time when the offer was created
    :accepted_by foreign_key: - the id of the user who accepted the offer
    '''
    __tablename__ = "com_offers"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable = True)
    kilometerpreis = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    accepted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    rating = db.relationship("Rating", backref='com_offer')


# Datenbank-Table für die Angebote der Fahrer
class DriverOffers(db.Model):
    '''represents a driver offer as a db table

    Columns
    :id primary_key: - the unique id of the driver_offer
    :location: - the location from where the driver wants to drive
    :start: - the start location, default: NULL, gets set by the location the
              user who accepts wants to start from
    :destination: - the destination location, default: NULL, gets set by the location the
              user who accepts wants to be driven to
    :vehicle: - the vehicle the driver drives with
    :created_at: - the date and time the offer was created
    :start_time: - the date and time the offer should be listed
    :valid_until: - the date and time the offer will be removed from the Offers
    :radius: - the radius around :location: the driver will take offers from
    :text: - a description of the offer with max 140 characters
    :accepted_at: - the date and time a user has accepted the offer
    :accepted_by foreign_key: - the foreign key associating the drive offer with the
                                user who accepted the offer by refering to its id
    '''

    __tablename__ = "driver_offers"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    start = db.Column(db.String(50), nullable = True)
    destination = db.Column(db.String(50), nullable = True)
    vehicle = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    start_time = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, default= "NULL")
    kilometerpreis = db.Column(db.Integer, nullable=False, default = 0)
    radius = db.Column(db.Integer, nullable = True)
    text = db.Column(db.String(140), nullable = True)
    accepted_at = db.Column(db.Integer, nullable = True)
    accepted_by = db.Column(db.Integer, db.ForeignKey('users.id'), default="NULL")

    rating = db.relationship("Rating", backref='drive_offer')
