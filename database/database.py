#!/usr/bin/env python3

""" The racer database. """

from typing import Type
from sqlalchemy.exc import NoResultFound

from . import DBStorage
from .models.user import User
from .models.message import Message


class Database(DBStorage):
    """ The racer database class. """
    def get_user(self, email: str) -> Type[User]:
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

    def get_user_by_reset_token(self, token: str) -> Type[User]:
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

    def find_host(self, bot_token: str) -> Type[User]:
        """ Get a user from the database by bot token """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(
                bot_token=bot_token
            ).one()

        except NoResultFound:
            raise NoResultFound from NoResultFound

        return user

    def update_bot_token(self, email: str, bot_token: str) -> None:
        """ Update the bot token """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(email=email).one()
            user.bot_token = bot_token
            session.flush()
            session.commit()

        except NoResultFound:
            raise NoResultFound from NoResultFound

    def delete_message(self, message_id: str) -> None:
        """ Deletes on message from a database
        """

        session = self.get_session()

        try:
            message = session.query(Message).filter_by(id=message_id).first()
            session.delete(message)
            session.flush()
            session.commit()

        except NoResultFound:
            raise NoResultFound from NoResultFound
