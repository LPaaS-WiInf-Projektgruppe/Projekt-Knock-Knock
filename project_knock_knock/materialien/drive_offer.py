
import datetime

class DriveOffer(object):
    def __init__(
            self, id, location, lat, long, vehicle, created_at, creator_id, creator_name, start_time,
            end_time, kilometerpreis, radius, text, rating, accepted_by_id, accepted_by_name):

        self.__id = id
        self.__location = location
        self.__lat = lat
        self.__long = long
        self.__vehicle = vehicle
        self.__created_at = created_at
        self.__creator_id = creator_id
        self.__creator_name = creator_name
        self.__start_time = start_time
        self.__end_time = end_time
        self.__kilometerpreis = kilometerpreis
        self.__radius = radius
        self.__text = text
        self.__rating = rating
        self.__accepted_by_id = accepted_by_id
        self.__accepted_by_name = accepted_by_name

    def set_id(self, location):
        self.__id = id

    def set_location(self, location):
        self.__location = location

    def set_lat(self, lat):
        self.__lat = lat

    def set_long(self, long):
        self.__long = long

    def set_vehicle(self, vehicle):
        self.__vehicle = vehicle

    def set_created_at(self, created_at):
        self.__created_at = created_at

    def set_creator_id(self, creator_id):
        self.__creator_id = creator_id

    def set_creator_name(self, creator_name):
        self.__creator_name = creator_name

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time

    def set_kilometerpreis(self, kilometerpreis):
        self.__kilometerpreis = kilometerpreis

    def set_radius(self, radius):
        self.__radius = radius

    def set_text(self, text):
        self.__text = text

    def set_rating(self, rating):
        self.__rating = rating

    def set_accepted_by_id(self, accepted_by_id):
        self.__accepted_by_id = accepted_by_id

    def set_accepted_by_name(self, accepted_by_name):
        self.__accepted_by_name = accepted_by_name


    def get_id(self):
        return self.__id

    def is_accepted(self):
        return self.__accepted_by_id != None

    def get_location(self):
        return self.__location

    def get_lat(self):
        return self.__lat

    def get_long(self):
        return self.__long

    def get_vehicle(self):
        return self.__vehicle

    def get_created_at(self):
        return self.__created_at

    def get_creator_id(self):
        return self.__creator_id

    def get_creator_name(self):
        return self.__creator_name

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_kilometerpreis(self):
        return self.__kilometerpreis

    def get_radius(self):
        return self.__radius

    def get_text(self):
        return self.__text

    def get_rating(self):
        return self.__rating

    def get_accepted_by_id(self):
        return self.__accepted_by_id

    def get_accepted_by_name(self):
        return self.__accepted_by_name

    def get_formatted_created_at_time(self):
        return self.__created_at.strftime("%H:%M")

    def get_formatted_created_at_date(self):
        return self.__created_at.strftime("%d.%m.%y")

    def get_formatted_start_time(self):
        return self.__start_time.strftime("%H:%M")

    def get_formatted_end_time(self):
        return self.__end_time.strftime("%H:%M")

    def get_formatted_start_date(self):
        return self.__start_time.strftime("%d.%m.%y")


    def get_formatted_end_date(self):
        return self.__end_time.strftime("%d.%m.%y")
