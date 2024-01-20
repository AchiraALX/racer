#!/usr/bin/env python3


""" The workers module. """


from typing import Dict

from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy.exc import NoResultFound, IntegrityError
from database.models.user import User
from database.database import Database


class AddToDBWorker():
    """ The add user worker class. """

    def add_user(self, user: Dict) -> Dict | None:
        """ Add user worker runner """
        _user = User(**user)
        db = Database()

        try:
            db.racer_add(_user)

        except IntegrityError:
            return None

        return user


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
def one_user(email: str) -> Dict | None:
    """ Query one user from the database """

    db = Database()
    try:
        user = db.get_user(email=email)

    except NoResultFound:
        return None

    return user
