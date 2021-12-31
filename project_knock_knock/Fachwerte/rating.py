class Rating(object):
    def __init__(self,value):

        # assert self.is_valid(value), "Rating List Cant be empty"
        self.__value = value

    def is_valid(self, rating):
        '''Checks if the rating has a valid value
        :param rating: the rating to check
        :return : True if the rating is valid
        '''

        return len(self.__value) > 0

    def get_rate_count(self):
        '''Returns the amount of Ratings for a User
        '''
        i = 0
        print("value: {}".format(self.__value))
        for value in self.__value:
            if value != None:
                i+= 1
        return i

    def calculate_average(self):
        '''Calculates the average over all ratings
        :param value_list: list of rating to calculate the
                     average of
        :return avg: the average of all ratings
        '''

        avg = 0
        kardinalitaet = 0
        for value in self.__value:
            if value != None:
                avg += value
                kardinalitaet +=1

        if kardinalitaet > 0:
            avg /= kardinalitaet
        else:
            return None

        return round(avg, 1)

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value
