#!/usr/bin/env python3


""" The workers module. """


from typing import Dict, Optional

from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy.exc import NoResultFound, IntegrityError
from database.models.user import User
from database.models.message import Message
from database.database import Database


class AddToDBWorker():
    """ The add user worker class. """

    def add_user(self, user: Dict) -> Optional[Dict]:
        """ Add user worker runner """
        _user = User(**user)
        db = Database()

        try:
            db.racer_add(_user)

        except IntegrityError:
            return None

        return user

    def add_message(self, message: dict) -> Optional[Dict]:
        """ Add message worker runner """
        _message = Message(**message)
        db = Database()

        try:
            db.racer_add(_message)

        except IntegrityError:
            return None

        return message


class UpdateDBWorker():
    """ The update user worker class. """

    def __init__(self, username: str, email: str, password: str) -> None:
        """ Update user worker constructor """
        self.username = username
        self.email = email
        self.password = password


# Hash the password using bcrypt
def hash_password(password: str) -> str:
    """ Hash the password """
    salt = gensalt(10)
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


# Check the password using bcrypt
def is_valid_password(password: str, hashed: str) -> bool:
    """ Check the password """
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def authenticate_user(email: str, password: str) -> bool:
    """ Authenticate the user """
    db = Database()
    try:

        user = db.get_user(email=email).__dict__

    except NoResultFound:
        return False

    success = is_valid_password(password, user['password'])

    return success


# Get a user
def one_user(email: str) -> Dict:
    """ Query one user from the database """

    db = Database()
    try:
        user = db.get_user(email=email)

    except NoResultFound:
        raise NoResultFound from NoResultFound

    return user.to_dict()


# Check if user exists
def user_exists(email: str) -> bool:
    """ Check if user exists """
    db = Database()
    try:
        db.get_user(email=email)

    except NoResultFound:
        raise NoResultFound from NoResultFound

    return True


# Update token if user exists
def update_reset_token(email: str, token: str) -> None:
    """ Update the reset token """

    # Check if user exists
    if not user_exists(email):
        raise NoResultFound from NoResultFound

    db = Database()
    try:
        db.update_reset_token(email, token)

    except NoResultFound:
        raise NoResultFound from NoResultFound


# Update password if user exists
def update_password(token: str, password: str) -> None:
    """ Update the password """
    db = Database()
    try:
        db.update_password(token, password)

    except NoResultFound:
        raise NoResultFound from NoResultFound


# Check for a valid token
def valid_token(token: str) -> bool:
    """ Check for a valid token """

    db = Database()
    try:
        db.get_user_by_reset_token(token)

    except NoResultFound:
        raise NoResultFound from NoResultFound

    return True


# Update the bot_token for a user
def update_bot_token(email: str, bot_token: str) -> None:
    """ Update the bot_token for a user """

    db = Database()
    try:
        db.update_bot_token(email, bot_token)

    except NoResultFound:
        raise NoResultFound from NoResultFound


# Find host by bot_token
def find_host(bot_token: str) -> Dict:
    """ Find host by bot_token """

    db = Database()
    try:
        host = db.find_host(bot_token)

    except NoResultFound:
        raise NoResultFound from NoResultFound

    return host.to_dict()
