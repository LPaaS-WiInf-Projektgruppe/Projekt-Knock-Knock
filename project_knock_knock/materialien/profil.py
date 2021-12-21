class Profil(object):
    '''Represents a User Profile with the following entities
    :param username: the name of the user
    :param working_times: the working times of a user
    :param rating: the average rating of a user
    :param description: a bio the user can set
    '''

    def __init__(self, username, working_times, user_accepted_drive_offers,
                          user_accepted_com_offers, rating, description):

        self.__username = username
        self.__working_times = working_times
        self.__rating = rating
        self.__description = description
        self.__user_accepted_drive_offers = user_accepted_drive_offers
        self.__user_accepted_com_offers = user_accepted_com_offers

    def get_username(self):
        return self.__username

    def get_working_times(self):
        return self.__working_times

    def get_rating(self):
        return self.__rating

    def get_description(self):
        return self.__decription

    def get_accepted_drive_offers(self):
        return self.__user_accepted_drive_offers

    def get_accepted_com_offers(self):
        return self.__user_accepted_com_offers

    def set_username(self, username):
        self.__username = username

    def set_working_times(self, working_time):
        self.__working_times = working_time

    def set_rating(self, rating):
        self.__rating = rating

    def set_description(self, description):
        self.__description = desciption

    def set_accepted_drive_offers(self, offers):
        self.__user_accepted_com_offers = offers

    def set_accepted_com_offers(self, offers):
        self.__user_accepted_drive_offers = offers
