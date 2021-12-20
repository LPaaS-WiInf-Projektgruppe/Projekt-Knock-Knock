class Profil(object):
    '''Represents a User Profile with the following entities
    :username: the name of the user
    :working_times: the working times of a user
    :rating: the average rating of a user
    :description: a bio the user can set
    '''

    def __init__(self, username, working_times, user_accepted_offers, rating, description):
        self.__username = username
        self.__working_times = working_times
        self.__rating = rating
        self.__description = description
        self.__user_accepted_offers = user_accepted_offers

    def get_username(self):
        return self.__username

    def get_working_times(self):
        return self.__working_times

    def get_rating(self):
        return self.__rating

    def get_description(self):
        return self.__decription

    def get_accepted_offers(self):
        return self.__user_accepted_offers

    def set_username(self, username):
        self.__username = username

    def set_working_times(self, working_time):
        self.__working_times = working_time

    def set_rating(self, rating):
        self.__rating = rating

    def set_description(self, description):
        self.__description = desciption

    def set_accepted_offers(self, offers):
        self.__user_accepted_offers = offers
