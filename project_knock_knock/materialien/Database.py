from sqlalchemy_utils import create_database, database_exists
from abc import ABC, abstractmethod
from config import SQLALCHEMY_DATABASE_URI


class Database(ABC):
    """ Represents a BaseDatabase"""
    def __init__(self, uri):
        self.__uri = uri

    @abstractmethod
    def add_database(self):
        pass

class SQLDatabase(Database):
    """represents a MariaDB database"""
    def __init__(self, uri):
        self.__uri = uri

    def add_database(self):
        SQLALCHEMY_DATABASE_URI = self.__uri.get_uri_string()

        if not database_exists(SQLALCHEMY_DATABASE_URI):
            create_database(SQLALCHEMY_DATABASE_URI)
