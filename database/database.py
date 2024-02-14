#!/usr/bin/env python3

""" The racer database. """

from typing import Type, Dict, Optional
from sqlalchemy.exc import NoResultFound, IntegrityError

from . import DBStorage
from .models.user import User
from .models.message import Message


class Database(DBStorage):
    """ The racer database class. """

    def save_user(self, user: User) -> Optional[User]:
        """Save user to database
        Arguments:
            user -> User

        Return:
            user -> User if save was successful
            None -> In case of any error
        """

        session = self.get_session()

        try:
            session.add(user)
            session.flush()
            session.commit()

            return user

        except IntegrityError:
            return None

    def save_message(self, message: Message) -> Optional[Message]:
        """Saving message to database

        Arguments:
            message -> Message

        Return:
            message -> Optional[Message] if success
            None -> In case of an error
        """

        session = self.get_session()

        try:
            session.add(message)
            session.flush()
            session.commit()
            self.close_session()

            return message

        except IntegrityError:
            return None

    def get_user(self, email: str) -> Type[User]:
        """ Get a user from the database """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(email=email).one()

        except NoResultFound:
            raise NoResultFound from NoResultFound

        return user

    def update_reset_token(self, email: str, token: str) -> Type[User]:
        """ Update the reset token """
        session = self.get_session()

        try:
            user = session.query(User).filter_by(email=email).one()
            user.password_reset_token = token
            session.flush()
            session.commit()

        except NoResultFound:
            raise NoResultFound from NoResultFound

        return user

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

    def update_user(self, fields: Dict, email: str) -> Type[User]:
        """Update user
        """

        session = self.get_session()

        try:
            user_to_update = session.query(User).filter_by(email=email).first()

            for key, val in fields.items():
                setattr(user_to_update, key, val)

        except NoResultFound:
            raise NoResultFound from NoResultFound

        return user_to_update

    def update_message(self, fields: Dict, message_id: str) -> Type[Message]:
        """Update message

        Arguments:
            fields -> Dict[str, Any]
            message_id -> str

        Return:
            Message -> Type[Message]
        """

        session = self.get_session()

        try:
            message_to_update = session.query(Message).filter_by(id=message_id).first()

            for key, val in fields.items():
                setattr(message_to_update, key, val)

        except NoResultFound:
            raise NoResultFound from NoResultFound

        return message_to_update
