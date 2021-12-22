class ComOffer(object):
    def __init__(self, id, start, destination, start_time, end_time,
        kilometerpreis, created_at, creator, rating):

        self.__id = id
        self.__start = start
        self.__destination = destination
        self.__start_time = start_time
        self.__end_time = end_time
        self.__kilometerpreis = kilometerpreis
        self.__created_at = created_at
        self.__creator = creator
        self.__rating = rating

    def set_id(self, id):
        self.__id = id

    def set_start(self, start):
        self.__start = start

    def set_destination(self, destination):
        self.__destination = destination

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time

    def set_kilometerpreis(self, kilometerpreis):
        self.__kilometerpreis = kilometerpreis

    def set_created_at(self, created_at):
        self.__created_at = created_at

    def set_creator(self, creator):
        self.__creator = creator

    def set_rating(self, rating):
        self.__rating = rating

    def get_id(self):
        return self.__id

    def get_start(self):
        return self.__start

    def get_destination(self):
        return self.__destination

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_kilometerpreis(self):
        return self.__kilometerpreis

    def get_created_at(self):
        return self.__created_at

    def get_creator(self):
        return self.__creator

    def get_rating(self):
        return self.__rating

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
