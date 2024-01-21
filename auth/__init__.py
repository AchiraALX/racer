#!/usr/bin/env python3


""" The racer authentication module. """

from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for
)
from flask_login import login_user, logout_user  # type: ignore
from sqlalchemy.exc import NoResultFound
from workers import (
    AddToDBWorker,
    hash_password,
    authenticate_user
)

add = AddToDBWorker()


racer_auth = Blueprint("racer_auth", __name__, url_prefix="/auth")


@racer_auth.route("/", methods=["GET", "POST"], strict_slashes=False)
def login():
    """ The racer login route handler. """

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            flash("Email is required")
            return redirect(url_for('racer_auth.login'))

        if not password:
            flash("Password is required")
            return redirect(url_for('racer_auth.login'))

        logged = authenticate_user(email, password)
        print(logged)

        if logged:
            from app import load_user

            try:
                user = load_user(email)
                login_user(user)

            except NoResultFound:
                flash("User not found")
                return redirect(url_for('racer_auth.login'))

            return redirect(url_for('index'))

        flash("Invalid email or password")
        return redirect(url_for('racer_auth.login'))

    return render_template('login.html')


@racer_auth.route("/logout", methods=["GET"], strict_slashes=False)
def logout():
    """ The racer logout route handler. """

    logout_user()
    return redirect(url_for('racer_auth.login'))


@racer_auth.route("/register", methods=["GET", "POST"], strict_slashes=False)
def register():
    """ The racer register route handler. """

    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if not username:
            flash("Username is required")
            return redirect(url_for('racer_auth.register'))

        if not email:
            flash("Email is required")
            return redirect(url_for('racer_auth.register'))

        if not password:
            flash("Password is required")
            return redirect(url_for('racer_auth.register'))

        if not confirm_password:
            flash("Confirm Password is required")
            return redirect(url_for('racer_auth.register'))

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('racer_auth.register'))

        user = {
            "username": username,
            "email": email,
            "password": hash_password(password)
        }

        try:
            add.add_user(user)
            flash("User created successfully")
            return redirect(url_for('racer_auth.login'))

        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for('racer_auth.register'))

    return render_template('sign-up.html')
