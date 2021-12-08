class Rating(object):
    def __init__(self,value):
        self.__value = value

    def get_rate_count(self, value_list):
        '''calculates the amount of ratings for a user
        '''
        return len(value_list)

    def calculate_average(self, value_list):
        '''calculates the average over all ratings
        :value_list: list of rating to calculate the
                     average of
        :avg: the average of all ratings
        '''
        for value in get_rate_count(value_list):
            avg += value

        avg /=  get_rate_count(value_list)

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
