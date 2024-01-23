#!/usr/bin/env python3

""" The racer main module. """

from flask import render_template, redirect, url_for, flash
from flask_login import login_required  # type: ignore
from . import racer


# Home racer
@racer.route("/", methods=["GET"], strict_slashes=False)
def index():
    """ The racer index route handler. """
    return render_template("racer.html")


# About racer
@racer.route("/about", methods=["GET"], strict_slashes=False)
def about():
    """ The racer about route handler. """
    return render_template("about.html")


# Help on racer
@racer.route("/help", methods=["GET"], strict_slashes=False)
def racer_help():
    """ The racer help route handler. """
    return render_template("help.html")


# Racer developer hire
@racer.route("/hire", methods=["GET"], strict_slashes=False)
def hire():
    """ The racer hire route handler. """
    return render_template("hire.html", hire=True)


@racer.route("/profile", methods=["GET"], strict_slashes=False)
@login_required
def profile():
    """ The racer profile route handler. """
    return render_template("profile.html")


@racer.errorhandler(404)
def page_not_found(error):
    """ The racer 404 error handler. """
    return f"404 error: {error}", 404


@racer.errorhandler(401)
def unauthorized(error):
    """ Error handler for unauthorized """

    flash(f"Login before accessing the page. {error}")
    return redirect(url_for('racer_auth.login'))
