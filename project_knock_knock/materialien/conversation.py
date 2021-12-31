class Conversation():
    '''Represents a Message between two Users
    :param id int: Unique identifier of a Message
    :param name String: The Username of the Sender
    :param zeit DateTime: The Date and Time of the message's creation
    :param gelesen bool: True - if the receiver has read the message, False - else
    '''
    def __init__(self, id, name, zeit, gelesen):
        self.__id = id
        self.__name = name
        self.__zeit = zeit
        self.__gelesen = gelesen

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_zeit(self):
        return self.__zeit

    def get_gelesen(self):
        return self.__gelesen


    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_zeit(self,zeit):
        self.__zeit = zeit

    def set_gelesen(self, gelesen):
        self.__gelesen = gelesen
