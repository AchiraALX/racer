#!/usr/bin/env python3


""" The racer main module. """

from secrets import token_urlsafe
from flask import Flask, redirect, url_for
from flask_login import LoginManager, UserMixin

from auth import racer_auth
from workers import one_user

racer = Flask(__name__)
racer.secret_key = token_urlsafe(16)
racer.debug = True

racer.register_blueprint(racer_auth)

login_manager = LoginManager(racer)


class User(UserMixin):
    """" The user mixin """
    def __init__(self, username: str, email: str, id: str):
        self.username = username
        self.email = email
        self.id = id


@login_manager.user_loader
def load_user(email):
    """ The racer user loader. """

    user = one_user(email)

    if user is None:
        return redirect(url_for('racer_auth.login'))

    return User(**user.to_dict())
