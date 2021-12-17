from Models import User


class DriveOffer(object):
    def __init__(
            self, id, location, vehicle, created_at, start_time, end_time,
            kilometerpreis, radius, text, rating, accepted_by):

        self.__id = id
        self.__location = location
        self.__vehicle = vehicle
        self.__created_at = created_at
        self.__start_time = start_time
        self.__end_time = end_time
        self.__kilometerpreis = kilometerpreis
        self.__radius = radius
        self.__text = text
        self.__rating = rating
        self.__accepted_by = accepted_by

    def set_id(self, location):
        self.__id = id

    def set_location(self, location):
        self.__location = location

    def set_vehicle(self, vehicle):
        self.__vehicle = vehicle

    def set_created_at(self, created_at):
        self.__created_at = created_at

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


    def get_id(self):
        return self.__id

    def set_accepted_by(self, accepted_by):
        self.__accepted_by = accepted_by

    def is_accepted(self):
        return self.__accepted_by != "NULL"


    def get_location(self):
        return self.__location

    def get_vehicle(self):
        return self.__vehicle

    def get_created_at(self):
        return self.__created_at

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

    def get_accepted_by(self):
        return self.__accepted_by

    def get_accepted_by_username(self):
        accepted_by = User.query.filter_by(id = self.__accepted_by).first()
        return accepted_by.username
