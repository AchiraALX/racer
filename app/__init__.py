#!/usr/bin/env python3


""" The racer main module. """

from secrets import token_urlsafe
from flask import Flask
from flask_login import LoginManager, UserMixin
from sqlalchemy.exc import NoResultFound

from auth import racer_auth

from workers import one_user

racer = Flask(__name__)
racer.secret_key = token_urlsafe(16)
racer.debug = False

racer.register_blueprint(racer_auth)


login_manager = LoginManager(racer)
login_manager.login_view = "racer_auth.login"


class User(UserMixin):
    """ The user class. """

    def __init__(self, username: str, email: str) -> None:
        """ The user constructor. """
        self.username = username
        self.email = email

    def get_id(self) -> str:
        """ Get the user id. """
        return self.email


@login_manager.user_loader
def load_user(user_id) -> User:
    """ Load the user. """

    logged_user = one_user(user_id)

    try:
        username = logged_user['username']
        email = logged_user['email']

    except NoResultFound:
        raise NoResultFound

    return User(
        username=username,
        email=email
    )
