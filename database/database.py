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

    def update_reset_token(self, email: str, token: str) -> None:
        """ Update the reset token """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(email=email).one()
            user.password_reset_token = token
            session.flush()
            session.commit()

        except NoResultFound:
            raise NoResultFound from NoResultFound

    def get_user_by_reset_token(self, token: str) -> User:
        """ Get a user from the database by reset token """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(
                password_reset_token=token
            ).one()

        except NoResultFound:
            raise NoResultFound from NoResultFound

        return user

    def update_password(self, token: str, password: str) -> None:
        """ Update the password """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(
                password_reset_token=token).one()
            user.password = password
            user.password_reset_token = None  # type: ignore
            session.flush()
            session.commit()

        except NoResultFound:
            raise NoResultFound from NoResultFound
