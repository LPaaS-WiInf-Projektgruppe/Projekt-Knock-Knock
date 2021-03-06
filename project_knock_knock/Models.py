from datetime import datetime, timedelta
from flask_user import UserMixin
from flask import request

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import distance

from sqlalchemy import Column, Integer, String, Boolean, Float, or_, and_
from sqlalchemy.sql import func

from extensions import db

from materialien.com_offer import ComOffer
from materialien.drive_offer import DriveOffer
from materialien.conversation import Conversation

from Fachwerte.rating import Rating as fw_rating
from Fachwerte.work_time import WorkTime as wt


working_time_identifier =  db.Table(
    "working_time_identifier",
    db.Column("working_time_id", db.Integer, db.ForeignKey("working_times.id")),
    db.Column("driver_offer_id", db.Integer, db.ForeignKey("users.id"))
)

class User(db.Model, UserMixin):
    '''Table that represents a User

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

    com_offers = db.relationship("ComOffers", foreign_keys='ComOffers.creator_id', backref= "creator")
    driver_offers = db.relationship("DriverOffers", foreign_keys='DriverOffers.creator_id', backref="creator")

    accepted_drive_offer = db.relationship("DriverOffers", foreign_keys='DriverOffers.accepted_by_user', backref='accepted_by')
    accepted_com_offer = db.relationship("ComOffers", foreign_keys='ComOffers.accepted_by_user', backref='accepted_by')

    messages_send = db.relationship(
        "ExchangedMessages",
        foreign_keys='ExchangedMessages.transmitter_id',
        backref="transmitter"
    )
    messages_rec = db.relationship(
        "ExchangedMessages",
        foreign_keys='ExchangedMessages.receiver_id',
        backref="receiver"
    )

    working_time = db.relationship(
            "WorkingTime",
            secondary = working_time_identifier,
            backref = db.backref("user", lazy="dynamic")
    )

    def get_conversations(user):
        '''Returns the Conversations of a User
        :param user User: The User object to get the conversations from
        :return toBeDisplayed List<Conversation>: A List containing the Conversations of a User
        '''

        # Ermittelt alle f??r den User relevanten Konversationen
        allParticipatedConversations = ExchangedMessages.query \
            .order_by(ExchangedMessages.created_at.desc()) \
            .filter(or_( \
                ExchangedMessages.transmitter == user,
                ExchangedMessages.receiver == user)) \
            .all()

        # Sammelt alle disjunkten bisherigen Kommunikationspartner
        allContacts = []
        for conversation in allParticipatedConversations:
            if conversation.transmitter not in allContacts:
                allContacts.append(conversation.transmitter)
            if conversation.receiver not in allContacts:
                allContacts.append(conversation.receiver)

        print("contacts: {}".format(allContacts))

        # Sammlung der jeweiligen Objekte ??ber die Kommunikationspartner
        toBeDisplayed = []

        # Erstellung der Objekte f??r die obige Sammlung
        for contact in allContacts:
            typ = User.query.filter_by(id = contact.id).first()
            try:
                zeit = ExchangedMessages.query \
                   .order_by(ExchangedMessages.created_at.desc()) \
                   .filter(or_(
                       and_(ExchangedMessages.transmitter == user,  ExchangedMessages.receiver == typ),
                       and_(ExchangedMessages.transmitter == typ, ExchangedMessages.receiver == user) \
                   )) \
                   .first().created_at

                gelesen = ExchangedMessages.query \
                    .order_by(ExchangedMessages.created_at.desc()) \
                        .filter( \
                            and_(ExchangedMessages.transmitter== typ, ExchangedMessages.receiver == user) \
                        ).first().read \

                infoRow  = Conversation(typ.id, typ.username, zeit, gelesen)
                toBeDisplayed.append(infoRow)
            except:
                pass
                # Auskommentierter Kommentar zum  Debuging, except und pass m??ssen aber bleiben
                # f??r den Fall von (noch) nicht existierenden Konversationen
                #return "Eigener Username: " + self.username + " und Nummer: " +str(self.id) + "\n" + "Andererer Dude: " + typ.username + " und Nummer: " +str(typ.id) + "\n" + "Letzte ausgetauschte Nachricht: " + "\n" + str(allContacts)


        return toBeDisplayed

class Rating(db.Model):
    ''' Represents the Rating of an Offer

    Columns
    :id primary_key: the unique identifier for the rating
    :stars: - the rating for an offer
    :drive_offer_id foreign_key: - the drive offer the rating belongs to
    :com_offer_id foreign_key: - the company offer the rating belongs to
    '''

    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable = True)
    com_offer = db.relationship("ComOffers", foreign_keys='ComOffers.rating_id', backref='rating')
    drive_offer = db.relationship("DriverOffers", foreign_keys='DriverOffers.rating_id', backref='rating')



    def get_user_rating(user):
        '''Get the Rating for a User from the database
        :param user User: A User object representing the User to get the rating for
        :return rating Rating: An Object containing the Ratings
        '''

        drive_offer_rating = db.session.query(DriverOffers) \
            .filter(DriverOffers.creator == user) \
            .all()

        com_offer_rating = db.session.query(ComOffers) \
            .filter(ComOffers.creator == user) \
            .all()

        # for r in drive_offer_rating[0]:
        #     print("rating:{}".format(r))

        ratings = []
        for r in drive_offer_rating:
            ratings.append(r.rating.stars)
        for r in com_offer_rating:
            ratings.append(r.rating.stars)

        rating = fw_rating(ratings)

        return rating

    def rate_offer(offer, type, form):
        '''Add a rating for an offer specified by 0 for DriveOffer and 1 for
         ComOFfer in combination with its unique ID
         :param offer int: The unique ID of an Offer
         :param type int: 0 for DriveOffer, 1 for ComOffer
         :param form dict: A Dictionary containing the form Rating data
        '''

        if type == 0:
            rating = Rating(stars = form)
            offer_to_rate = DriverOffers.query.filter_by(id = offer).first()
            offer_to_rate.rating = rating
            offer_to_rate.completed_at = datetime.now()
            db.session.add(rating)

        else:
            rating = Rating(stars = form)
            offer_to_rate = ComOffers.query.filter_by(id = offer).first()
            offer_to_rate.rating = rating
            offer_to_rate.completed_at = datetime.now()
            db.session.add(rating)

        db.session.commit()

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
    start_time = db.Column(db.String(5), nullable = True)
    end_time = db.Column(db.String(5), nullable = True)
    weekday = db.Column(db.Integer, nullable= True)


    def get_worktime_for_user(user):
        '''Query database for every entry that belongs to the user and
        :param user int: id of a user
        :return work_times list<WorkTime>: A list containing the WorkTimes of a user
        '''
        result = db.session.query(User, WorkingTime) \
            .join(WorkingTime.user) \
            .filter_by(username = user.username) \
            .order_by(WorkingTime.weekday) \
            .all()

        work_times = []
        for user, work_time in result:
            work_time = wt(
                work_time.weekday,
                work_time.start_time,
                work_time.end_time
            )
            work_times.append(work_time)

        return work_times

class ComOffers(db.Model):
    '''Represents a Company Offer as a DB table

    Columns
    :id primary_key: - the unique identifier for the company offer
    :start: - the start location of the offer
    :start_lat: - The latitude of the start location
    :start_long: - The Longitude Coordinate of the start location
    :end_lat: - The latitude of the end location
    :end_long: - The Longitude of the end location
    :destination: - the destination of the offer
    :start_time: - the date and time when the offer is starting
    :end_time: - the date and time when the offer is ending is
                 default = start_time
    :kilometerpreis: - the price the user who created the offer
                       is willing to pay per kilometer
    :created_at: the date and time when the offer was created
    :ended_at: the time the offer has been given a rating
    :accepted_by foreign_key: - the id of the user who accepted the offer
    '''
    __tablename__ = "com_offers"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(50), nullable=False)
    start_lat = db.Column(db.Float, nullable=False)
    start_long = db.Column(db.Float, nullable=False)
    end_lat = db.Column(db.Float, nullable=False)
    end_long = db.Column(db.Float, nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable = True)
    kilometerpreis = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    completed_at = db.Column(db.DateTime, nullable=True)
    accepted_by_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating_id = db.Column(db.Integer, db.ForeignKey("ratings.id"))

    def get_available_offers():
        '''Returns the all ComOffers that have not been accepted
        :return com_offers List<ComOffer>: The List of ComOffers
        '''

        allComOffers = db.session.query(ComOffers) \
            .filter(ComOffers.accepted_by == None) \
            .all()

        com_offers = []
        for  com_offer in allComOffers:
            format_start_time = com_offer.start_time.strftime("%d.%m.%y %H:%M")
            format_end_time = com_offer.end_time.strftime("%d.%m.%y %H:%M")
            com_offer = ComOffer(
                com_offer.id,
                com_offer.start,
                com_offer.destination,
                format_start_time,
                format_end_time,
                com_offer.kilometerpreis,
                com_offer.created_at,
                com_offer.id,
                com_offer.rating,
                # TODO: completed_at
                # TODO: add description
                com_offer.rating.stars,
                # TODO: add accepted_by
            )
            com_offers.append(com_offer)
        print("com_offers: {}".format(com_offers))

        return com_offers

    def delete_offer(id):
        '''Delete the Com Offer with the specified id
        :param id int: the id of the com offer to delete
        :return bool: True, if offer was deleted
                      False, if offer could not be deleted
        '''

        comOffer_to_delete = ComOffers.query.get_or_404(id)
        try:
            if comOffer_to_delete.accepted_by == None:
                db.session.delete(comOffer_to_delete)
                db.session.commit()
                return True
            else:
                return False
        except:
            return False

    def accept_offer(id, curr_user):
        '''Accept the offer with the provided id
        :param id int: the id of the offer to accept
        :param curr_user User: An object representing the current User
        :return bool: True, if offer was accepted
                      False, if offer could not be deleted
        '''

        com_offer = db.session.query(ComOffers) \
            .filter(ComOffers.id == id) \
            .first()

        if com_offer.creator.id != curr_user.id:
            com_offer.accepted_by = curr_user
            db.session.commit()
            return True
        else:
            return False

    def create_offer(form, user):
        '''Create a Com Offer with the data submitted with the form and
         associates a user with the Com Offer
         :param form dict: a dict with the contents of the offer
         :param user User: a User object to associate the offer with
         :return bool: True, if the offer was created successfully
                       False, if offer could not be created
        '''
        content_start = form.von.data
        content_ende = form.nach.data
        content_start_zeit = form.zeit_start.data
        content_end_zeit = form.zeit_ende.data
        content_geld = form.geld.data


        # geocode the location
        # geolocator = Nominatim(user_agent="project_knock_knock")
        # start_location = geolocator.geocode(content_start)
        # end_location = geolocator.geocode(content_ende)

        locations = [content_start, content_ende]
        start_location, end_location = DriverOffers.geocode_location(locations)


        # TODO: currently end time needs to be filled in to submit the form
        if content_end_zeit == "":
            com_offer = ComOffers(
                start = content_start,
                start_lat = start_location.latitude,
                start_long = start_location.longitude,
                end_lat = end_location.latitude,
                end_long = end_location.longitude,
                destination = content_ende,
                start_time = content_start_zeit,
                kilometerpreis = content_geld,
                creator = user,
                rating = Rating()
            )
        else:

            com_offer = ComOffers(
                start = content_start,
                start_lat = start_location.latitude,
                start_long = start_location.longitude,
                end_lat = end_location.latitude,
                end_long = end_location.longitude,
                destination = content_ende,
                start_time = content_start_zeit,
                end_time = content_end_zeit,
                kilometerpreis = content_geld,
                creator = user,
                rating = Rating()
            )

        # rating = Rating()

        try:
            db.session.add(com_offer)
            # db.session.add(rating)
            db.session.commit()
            return True
        except:
            return False

    def get_user_accepted_offers(user):
        '''Return the DriveOffers a User accepted
        :param user User: A User object representing the User
        :return user_accepted_com_offers List<ComOffer>: A List containing the ComOffers of a user
        '''
        # query database for every company offer that the user accepted
        user_accepted_com_offers_query = db.session.query(ComOffers) \
            .filter(ComOffers.completed_at == None) \
            .all()

        user_accepted_com_offers = []
        for com_offer in user_accepted_com_offers_query:
            if com_offer.accepted_by != None:
                if com_offer.accepted_by.id == user.id:
                    user_accepted_com_offer = ComOffer(
                        com_offer.id,
                        com_offer.start,
                        com_offer.destination,
                        com_offer.start_time,
                        com_offer.end_time,
                        com_offer.kilometerpreis,
                        com_offer.created_at,
                        com_offer.creator,
                        com_offer.accepted_by.username,
                        com_offer.rating.stars
                    )
                    user_accepted_com_offers.append(user_accepted_com_offer)

        return user_accepted_com_offers

    def get_user_created_offers(user):
        '''Returns the ComOffers a User created
        :param user User: A User Object representing the current User
        :return drive_offers List<ComOffer>: A List of ComOffers
        '''

        results = db.session.query(ComOffers) \
            .filter(ComOffers.completed_at == None) \
            .all()

        com_offers = []
        for offer in results:
            if offer.creator.id == user.id:
                if offer.completed_at == None:
                    com_offer = ComOffer(
                        offer.id,
                        offer.start,
                        offer.destination,
                        offer.start_time,
                        offer.end_time,
                        offer.kilometerpreis,
                        offer.created_at,
                        offer.creator.id,
                        offer.creator.username,
                        # TODO: add a text field for ComOffers
                        # offer.text,
                        offer.rating.stars
                    )
                    com_offers.append(com_offer)

        return com_offers

    def get_all_coordinates():
        '''Returns a list of all the coordinates of The COmOffers
        :return coordinates List<List<int, List<int>>>: A List Containing a List
        with the Latitude and longitude and the id of the offer
        '''
        com_offers = ComOffers.query.all()
        coordinates = []
        for offer in com_offers:
            coordinates.append([offer.id, [offer.start_lat, offer.start_long], [offer.end_lat, offer.end_long]])
        return coordinates

    def get_offer(id):
        '''Returns the ComOffer specified by the ID
        :param id int: The ID of the ComOffer to get
        :return drive_offer ComOffer: The Object of the ComOffer specified by the ID
        '''

        com_offer = db.session.query(ComOffers) \
            .filter(ComOffers.id == id) \
            .first()

        com_offer = ComOffer(
            com_offer.id,
            com_offer.start,
            com_offer.destination,
            com_offer.start_time,
            com_offer.end_time,
            com_offer.kilometerpreis,
            com_offer.created_at,
            com_offer.creator.id,
            com_offer.creator.username,
            # TODO: completed_at
            # TODO: add description
            com_offer.rating.stars
            # TODO: add accepted_by
        )

        return com_offer

# Datenbank-Table f??r die Angebote der Fahrer
class DriverOffers(db.Model):
    '''Represents a driver offer as a db table

    Columns
    :id primary_key: - the unique id of the driver_offer
    :location: - the location from where the driver wants to drive
    :lat: The Latitude of the Location
    :long: The Longitude of the Location
    :start: - the start location, default: NULL, gets set by the location the
              user who accepts wants to start from
    :destination: - the destination location, default: NULL, gets set by the location the
              user who accepts wants to be driven to
    :vehicle: - the vehicle the driver drives with
    :created_at: - the date and time the offer was created
    :ended_at: the time the offer has been given a rating
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
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    start = db.Column(db.String(50), nullable = True)
    destination = db.Column(db.String(50), nullable = True)
    vehicle = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    completed_at = db.Column(db.DateTime, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=True)
    kilometerpreis = db.Column(db.Integer, nullable=False, default = 0)
    radius = db.Column(db.Integer, nullable = True)
    text = db.Column(db.String(140), nullable = True)
    accepted_at = db.Column(db.Integer, nullable = True)
    accepted_by_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating_id = db.Column(db.Integer, db.ForeignKey("ratings.id"))


    def get_offers():
        '''Returns all DriveOffers that have not been accepted
        :return drive_offers List<DriveOffer>: A List containing the DriveOffer objects
        '''
        allDriverOffers = DriverOffers.query \
            .filter_by(accepted_by = None) \
            .order_by(DriverOffers.id) \
            .all()

        drive_offers = []

        for  drive_offer in allDriverOffers:
            if drive_offer.accepted_by == None:
                drive_offer = DriveOffer(
                    drive_offer.id,
                    drive_offer.location,
                    drive_offer.lat,
                    drive_offer.long,
                    drive_offer.vehicle,
                    drive_offer.created_at,
                    drive_offer.creator,
                    drive_offer.creator.username,
                    drive_offer.start_time,
                    drive_offer.valid_until,
                    drive_offer.kilometerpreis,
                    drive_offer.radius,
                    drive_offer.text,
                    drive_offer.rating.stars,
                    None,
                    None
                )
                drive_offers.append(drive_offer)

            else:
                drive_offer = DriveOffer(
                    drive_offer.id,
                    drive_offer.location,
                    drive_offer.lat,
                    drive_offer.long,
                    drive_offer.vehicle,
                    drive_offer.created_at,
                    drive_offer.creator,
                    drive_offer.creator.username,
                    drive_offer.start_time,
                    drive_offer.valid_until,
                    drive_offer.kilometerpreis,
                    drive_offer.radius,
                    drive_offer.text,
                    drive_offer.rating.stars,
                    drive_offer.accepted_by.id,
                    drive_offer.accepted_by.username
                )
                drive_offers.append(drive_offer)

        return drive_offers

    def delete_offer(offer):
        '''Delete the DriveOffer specified by the ID
        :param offer int: The ID of the DriveOffer to delete
        :return bool: True, if the DriveOffer was deleted successfully
                      False, else
        '''
        driverOffer_to_delete = DriverOffers.query.get_or_404(offer)
        try:
            if driverOffer_to_delete.accepted_by == None:
                db.session.delete(driverOffer_to_delete)
                db.session.commit()
                return True
            else:
                return False
        except:
            return False

    def accept_offer(offer_id, user):
        '''Accept the DriveOffer specified by the ID
        :param offer_id int: The ID of the DriveOffer to delete
        :param user User: The User Object of the User accepting the offer
        :return bool: True, if the DriveOffer was deleted successfully,
                      False, else
        '''

        # TODO: contact users who accepted an offer

        drive_offer = db.session.query(DriverOffers) \
            .filter(DriverOffers.id == offer_id) \
            .first()

        # Check if the creator of the drive offer is the current user
        # to prevent users from accepting their own offers
        if drive_offer.creator.id != user.id:
            drive_offer.accepted_by = user
            db.session.commit()
            return True
        else:
            return False

    def create_offer(form, user):
        '''Create a DriveOffer from the data submitted with the form and
         associates a user with the DriveOffer
         :param form dict: a dict with the contents of the offer
         :param user User: a User object to associate the offer with
         :return bool: True, if the offer was created successfully
                       False, if offer could not be created
        '''

        content_ort = form.ort.data
        content_fahrzeug = form.fahrzeug.data
        content_start_zeit = form.zeit_start.data
        content_end_zeit = form.zeit_ende.data
        content_preis = form.preis.data
        content_radius = form.radius.data
        content_text = form.bemerkungen.data

        # geocode the location
        geolocator = Nominatim(user_agent="project_knock_knock")
        location = geolocator.geocode(content_ort)




        i = 0
        start_times = []
        end_times = []
        for results in form:

            # TODO: fix datetime.datetime object is not subscriptable

            print("results: {}:{}".format(results.id, results.data))
            if (results.id == "from_zeitMo" or results.id == "from_zeitDi" or results.id == "from_zeitMi" or \
                results.id == "from_zeitDo" or results.id == "from_zeitFr" or results.id == "from_zeitSa" or \
                results.id == "from_zeitSo"):

                start_times.append(results.data)

            if (results.id == "to_zeitMo" or results.id == "to_zeitDi" or results.id == "to_zeitMi" or \
                results.id == "to_zeitDo" or results.id == "to_zeitFr" or results.id == "to_zeitSa" or \
                results.id == "to_zeitSo"):

                end_times.append(results.data)

        working_times = []
        for i in range(len(start_times)):
            working_time = WorkingTime(
                weekday = i,
                start_time = start_times[i].strftime("%H:%M"),
                end_time = end_times[i].strftime("%H:%M")
            )
            working_time.user.append(user)
            db.session.add(working_time)
            i+=1


        driver_offer = DriverOffers(
            location = content_ort,
            lat = location.latitude,
            long = location.longitude,
            vehicle = content_fahrzeug,
            start_time = content_start_zeit,
            valid_until = content_end_zeit,
            kilometerpreis = content_preis,
            radius = content_radius,
            text = content_text,
            creator = user,
            rating = Rating()
        )

        # try:
        db.session.add(driver_offer)
        db.session.commit()
        return True
        # except:
        #     return False

    def get_user_accepted_offers(user):
        '''Query database for every drive offer that the user accepted
        :param user User: The User object of the User accepting the DriveOffer
        :return user_accepted_drive_offers List<DriveOffer>: A list containing
                                                             the DriveOffers of a User
        '''
        user_accepted_drive_offers_query = db.session.query(DriverOffers) \
            .filter(DriverOffers.completed_at == None) \
            .all()

        # print("accepted drive offers: {} \n" \
        #     "accepted company offers:"
        #     .format(user_accepted_drive_offers))

        user_accepted_drive_offers = []
        for drive_offer in user_accepted_drive_offers_query:
            if drive_offer.accepted_by_user == user.id:
                user_accepted_drive_offer = DriveOffer(
                    drive_offer.id,
                    drive_offer.location,
                    drive_offer.lat,
                    drive_offer.long,
                    drive_offer.vehicle,
                    drive_offer.created_at,
                    drive_offer.creator,
                    drive_offer.creator.username,
                    drive_offer.start_time,
                    drive_offer.valid_until,
                    drive_offer.kilometerpreis,
                    drive_offer.radius,
                    drive_offer.text,
                    drive_offer.rating.stars,
                    drive_offer.accepted_by.id,
                    drive_offer.accepted_by.username
                )
                user_accepted_drive_offers.append(user_accepted_drive_offer)

        return user_accepted_drive_offers

    def get_user_created_offers(user):
        '''Returns the DriveOffers a User created
        :param user User: The User Object of the User who created the DriveOFfer
        :return com_offers List<DriveOffer>: A List of DriveOffers
        '''

        results = db.session.query(DriverOffers) \
            .filter(DriverOffers.completed_at == None) \
            .all()



        drive_offers = []
        for offer in results:
            if offer.accepted_by == None:
                if offer.creator.id == user.id:
                    drive_offer = DriveOffer(
                        offer.id,
                        offer.location,
                        offer.lat,
                        offer.long,
                        offer.vehicle,
                        offer.created_at,
                        offer.creator,
                        offer.creator.username,
                        offer.start_time,
                        offer.valid_until,
                        offer.kilometerpreis,
                        offer.radius,
                        offer.text,
                        offer.rating.stars,
                        None,
                        None
                    )
                    drive_offers.append(drive_offer)
            else:
                if offer.creator.id == user.id:
                    drive_offer = DriveOffer(
                        offer.id,
                        offer.location,
                        offer.lat,
                        offer.long,
                        offer.vehicle,
                        offer.created_at,
                        offer.creator,
                        offer.creator.username,
                        offer.start_time,
                        offer.valid_until,
                        offer.kilometerpreis,
                        offer.radius,
                        offer.text,
                        offer.rating.stars,
                        offer.accepted_by.id,
                        offer.accepted_by.username
                    )
                    drive_offers.append(drive_offer)

        print("user_created_drive_offerss: {}".format(drive_offers))
        return drive_offers

    def get_offer(offer_id):
        '''Returns the DriveOffer specified by the ID
        :param user User: The ID of the DriveOffer to get
        :return drive_offer DriveOffer: The Object of the DriveOffer specified by the ID
        '''

        drive_offer = db.session.query(DriverOffers) \
            .filter(DriverOffers.id == offer_id) \
            .first()



        if drive_offer.accepted_by == None:
            drive_offer = DriveOffer(
                drive_offer.id,
                drive_offer.location,
                drive_offer.lat,
                drive_offer.long,
                drive_offer.vehicle,
                drive_offer.created_at,
                drive_offer.creator.id,
                drive_offer.creator.username,
                drive_offer.start_time,
                drive_offer.valid_until,
                drive_offer.kilometerpreis,
                drive_offer.radius,
                # TODO: add actual text
                "driver_offer.text",
                drive_offer.rating.stars,
                None,
                None
            )
        else:
            drive_offer = DriveOffer(
                drive_offer.id,
                drive_offer.location,
                drive_offer.lat,
                drive_offer.long,
                drive_offer.vehicle,
                drive_offer.created_at,
                drive_offer.creator.id,
                drive_offer.creator.username,
                drive_offer.start_time,
                drive_offer.valid_until,
                drive_offer.kilometerpreis,
                drive_offer.radius,
                # TODO: add actual text
                "driver_offer.text",
                drive_offer.rating.stars,
                drive_offer.accepted_by.id,
                drive_offer.accepted_by.username
            )

        return drive_offer

    def geocode_location(locations):
        '''Convert the given locations to their respective lat long Coordinates
        :param locations List<String>: A List containing the String
        representations of the locations
        :return locations List<Location>: A List containing Geopy Location Objects
        (address<String>, (latitude<Float>, longitude<Float>))
        '''

        geolocator = Nominatim(user_agent="project_knock_knock")
        rate_limiter = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        locations = [rate_limiter(loc, language="de") for loc in locations]

        # start_location = (locations[0].latitude, locations[0].longitude)
        # end_location = (locations[1].latitude, locations[1].longitude)

        return locations

    def search_offer_by_location(start, end):
        '''Search suiting DriverOffers for the provided Route
        :param start String: The start location of the Route
        :param end String: The end location of the route
        :return filtered_drive_offers List<DriverOffer>: A List containing the offers that have
        radius within the start and end parameters
        '''

        # get all relevant DriveOffers
        drive_offers = DriverOffers.get_offers()

        # geocode the start and end locations
        locations = DriverOffers.geocode_location([start, end])
        start_location = (locations[0].latitude, locations[0].longitude)
        end_location = (locations[1].latitude, locations[1].longitude)

        # check if the distance between start and end location of an offer is
        # smaller than the radius of the DriveOffer for all DriveOffers
        filtered_drive_offers = []
        for drive_offer in drive_offers:
            offer_location = (drive_offer.get_lat(), drive_offer.get_long())
            print("distance:\nstart -> offer: {}\nend -> offer: {}\nradius: {}" \
                .format(
                    distance(offer_location, start_location).km,
                    distance(offer_location, end_location).km,
                    drive_offer.get_radius()
                ))

            if (distance(offer_location, start_location).km < drive_offer.get_radius()) and \
               (distance(offer_location, end_location).km < drive_offer.get_radius()):


               filtered_drive_offers.append(drive_offer)

        print("filtered_drive_offers: {}".format(filtered_drive_offers))

        return filtered_drive_offers


        # coord_locations = []
        # for drive_offer in drive_offers:
            # location = geolocator.geocode(drive_offer.get_location())
            # lat.append((location.lat, location.long))

class ExchangedMessages(db.Model):
    '''Database Table for Messages Exchanged between users

    Columns
    :id: the unique identifier for the Message
    :transmitter: the id of the User who transmitted the message
    :receiver: the id of the User who received the message
    :created_at: timestamp of the point the message was send?
    :read: True if message has been read, False else
    '''
    __tablename__ = "exchanged_messages"
    id = db.Column(db.Integer, primary_key=True)
    transmitter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    text = db.Column(db.String(200), nullable = False)
    read = db.Column(db.Boolean, nullable = False)



    def get_messages_for_user(user, other_user):

            dude = User.query.filter_by(id = other_user.id).first()

            if request.method == 'POST' :
                content_text = request.form['send']
                new_message = ExchangedMessages(
                    transmitter = user,
                    receiver = dude,
                    text = content_text,
                    read = False
                )

                try:
                    db.session.add(new_message)
                    db.session.commit()
                    return redirect("/chat/" + str(dude.id))
                except:
                    return 'Nachricht konnte nicht versendet werden :/'

            else:
                #messages = ExchangedMessages.query.order_by(ExchangedMessages.created_at).filter(and_(
                #            or_(ExchangedMessages.transmitter == dude.id),
                #            or_(ExchangedMessages.transmitter == self.id),
                #            or_(ExchangedMessages.receiver == dude.id),
                #            or_(ExchangedMessages.receiver == self.id))
                #            ).all()


                # Setzen des Status der Nachrichten auf gelesen, da sie im Anschluss ge??ffnet werden
                # Try Block, da nicht immer schon welche vorhanden
                try:
                    message = ExchangedMessages.query.order_by(ExchangedMessages.created_at.desc()).filter(
                                and_(ExchangedMessages.transmitter == dude, ExchangedMessages.receiver == user)
                                ).first()
                    gelesen = ExchangedMessages.query.filter(ExchangedMessages.id == message.id).first().read

                    if gelesen == False:
                        ExchangedMessages.query.filter(ExchangedMessages.id == message.id).update({"read": True})
                        db.session.commit()
                except:
                    pass

                # ??bergabe der Nachrichten aus dem ausgew??hlten Chat
                messages = ExchangedMessages.query.order_by(ExchangedMessages.created_at).filter(or_(
                        and_(ExchangedMessages.transmitter == dude, ExchangedMessages.receiver == user),
                        and_(ExchangedMessages.transmitter == user, ExchangedMessages.receiver == dude)
                            )).all()

                return messages
