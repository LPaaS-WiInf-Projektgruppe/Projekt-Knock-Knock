class Rating(object):
    def __init__(self,value):
        self.__value = value

    def is_valid(self, rating):
        '''
        checks if the rating has a valid value
        :param rating: the rating to check
        :return : True if the rating is valid
        '''

        return len(self.__value) > 0



    def get_rate_count(self):
        '''calculates the amount of ratings for a user
        '''
        return len(self.__value)

    def calculate_average(self):
        '''calculates the average over all ratings
        :value_list: list of rating to calculate the
                     average of
        :avg: the average of all ratings
        '''

        assert self.is_valid(self.__value), "Cant compute the average of an empty list."

        avg = 0
        for value in self.__value:
            avg += value

        avg /=  self.get_rate_count()
        return avg

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
