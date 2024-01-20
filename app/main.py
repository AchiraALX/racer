#!/usr/bin/env python3

""" The racer main module. """

from flask import render_template
from . import racer


@racer.route("/", methods=["GET"], strict_slashes=False)
def index():
    """ The racer index route handler. """
    return render_template("racer.html")


@racer.errorhandler(404)
def page_not_found(error):
    """ The racer 404 error handler. """
    return f"404 error: {error}", 404
