class WorkTime(object):
    '''Represents a the Working Time for a specific day
    :day:
    :start_time: time when driver starts working
    :end_time: time when user ends working
    '''
    def __init__(self, weekday, start_time, end_time):
        self.__weekday = weekday
        self.__start_time = start_time
        self.__end_time = end_time


    def weekday_to_string_short(self):

        if self.__weekday == 0:
            weekday = "Mo"
        if self.__weekday == 1:
            weekday = "Di"
        if self.__weekday == 2:
            weekday = "Mi"
        if self.__weekday == 3:
            weekday = "Do"
        if self.__weekday == 4:
            weekday = "Fr"
        if self.__weekday == 5:
            weekday = "Sa"
        if self.__weekday == 6:
            weekday = "So"
        return weekday

    def set_weekday(self, weekday):
        self.__weekday = weekday

    def set_start_time(self, start_time):
        self.__start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time

    def get_weekday(self):
        return self.__weekday

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time
