#!/usr/bin/env python3

""" The racer database. """


from sqlalchemy.exc import NoResultFound

from . import DBStorage
from .models.user import User


class Database(DBStorage):
    """ The racer database class. """
    def get_user(self, email: str) -> User:
        """ Get a user from the database """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(email=email).one()

        except NoResultFound:
            raise NoResultFound from NoResultFound

        return user
