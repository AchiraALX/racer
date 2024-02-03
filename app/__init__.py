#!/usr/bin/env python3


""" The racer main module. """

from secrets import token_urlsafe
from flask import Flask, url_for, redirect
from flask_login import LoginManager, UserMixin  # type: ignore
from flask_cors import CORS  # type: ignore
from flask_moment import Moment  # type: ignore
from sqlalchemy.exc import NoResultFound

from auth import racer_auth
from api.v1 import racer_api

from workers import one_user

racer = Flask(__name__)
racer.secret_key = token_urlsafe(16)
racer.debug = True
CORS(racer, resources={r"/*": {"origins": "*"}})
moment = Moment(racer)

racer.register_blueprint(racer_auth)
racer.register_blueprint(racer_api)


login_manager = LoginManager(racer)
login_manager.login_view = "racer_auth.login"


class User(UserMixin):
    """ The user class. """

    def __init__(
        self, username: str, email: str, _id: str, bot_token: str
    ) -> None:
        """ The user constructor. """
        self.username = username
        self.email = email
        self._id = _id
        self.bot_token = bot_token

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
        _id = logged_user['id'],
        bot_token = logged_user['botToken']

    except NoResultFound:
        return redirect(url_for("racer_auth.login"))  # type: ignore

    return User(
        username=username,
        email=email,
        _id=_id,  # type: ignore
        bot_token=bot_token
    )
