#!/usr/bin/env python3


""" The workers' module. """


import datetime
import json
from typing import Dict, Optional, Type, Any, List, Set, TypeVar

from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from database.models.user import User
from database.models.message import Message
from database.database import Database
from .redis import Cache


def add_message(message: dict) -> Optional[Dict]:
    """ Add message worker runner """
    _message = Message(**message)
    db = Database()

    try:
        db.racer_add(_message)

    except IntegrityError:
        raise IntegrityError from IntegrityError

    return message


def add_user(user: Dict) -> Optional[User]:
    """ Add user worker runner """
    _user = User(**user)
    db = Database()

    user = db.save_user(_user)

    if user is None:
        return None

    return user


def update_message(fields: Dict[str, Any], message_id: str) -> Type[Message]:
    """Update message

    fields: -> Message field to update [str, Any]
    message_id: -> Message id

    Return:
        message -> Type[Message]
    """

    db = Database()
    try:
        message = db.update_message(fields=fields, message_id=message_id)

    except NoResultFound:
        raise NoResultFound from NoResultFound

    return message


def update_user(fields: Dict, email: str) -> Type[User]:
    """Update user details

    fields -> Dict
    """

    db = Database()

    try:
        user = db.update_user(fields=fields, email=email)

    except NoResultFound:
        raise NoResultFound from NoResultFound

    return user


# Hash the password using bcrypt
def hash_password(password: str) -> str:
    """Hash the password

    Arguments:
        password -> str
    """
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
def one_user(email: str) -> Dict[str, Any]:
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


# From redis to server if message time > 12 hours
def to_database() -> None:
    """ From redis to server if message time > 12 hours """

    cache = Cache()
    messages = cache.get_all_messages()

    for message in messages:
        message = message.decode('utf-8')
        message = json.loads(message)

        message_time = datetime.datetime.fromisoformat(message['dtime'])

        if (datetime.datetime.now() - message_time).seconds > 43200:
            add_message(message)
            cache.delete_message(message['id'])


# Get conversations
def get_conversations(messages: List) -> List:
    """ Get the available conversations """

    unique = develop_guests(messages=messages)
    cache = Cache()
    conversations = []

    for token in unique:
        conversations.append(
            cache.retrieve_messages(token=token)
        )

    new_conversations = []
    for conversation in conversations:
        new_conversations.append(
            max(
                conversation,
                key=lambda x: datetime.datetime.fromisoformat(x['dtime']))
        )

    return new_conversations


# Develop guests
def develop_guests(messages: List) -> Set:
    """ Return a set of unique guests """

    guests = set()

    for message in messages:
        if message['client'] == 'guest':
            guests.add(message['frm'])

        if message['client'] == ' host':
            guests.add(message['to'])

    return guests
