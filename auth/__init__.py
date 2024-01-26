#!/usr/bin/env python3


""" The racer authentication module. """

import secrets
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for
)
from flask_login import login_user, logout_user, current_user  # type: ignore
from sqlalchemy.exc import NoResultFound, DBAPIError
from workers import (
    AddToDBWorker,
    hash_password,
    authenticate_user,
    user_exists,
    update_reset_token,
    valid_token,
    update_password
)

add = AddToDBWorker()


racer_auth = Blueprint("racer_auth", __name__, url_prefix="/auth")


@racer_auth.route("/", methods=["GET", "POST"], strict_slashes=False)
def login():
    """ The racer login route handler. """

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

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

        if logged:
            from app import load_user

            try:
                user = load_user(email)
                login_user(user)

            except NoResultFound:
                flash("User not found. Sign up to continue")
                return redirect(url_for('racer_auth.register'))

            return redirect(url_for('dashboard'))

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

    if current_user.is_authenticated:
        return redirect(url_for('index'))

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

        except DBAPIError as exc:
            flash(f"Error: {exc}")
            return redirect(url_for('racer_auth.register'))

    return render_template('sign-up.html')


@racer_auth.route(
    "/reset-token", methods=["GET", "POST"], strict_slashes=False)
def reset_token():
    """ The racer reset password route handler. """

    if request.method == 'POST':
        email = request.form.get("email")

        if not email:
            flash("Email is required")
            return redirect(url_for('racer_auth.reset_token'))

        try:
            user_exists(email)
            token = secrets.token_hex(16)

            try:
                update_reset_token(email, token)
                flash("Reset token sent to your email")
                return redirect(
                    url_for('racer_auth.save_new_password', token=token))

            except NoResultFound:
                flash("User not found")
                return redirect(url_for('racer_auth.reset_token'))

        except NoResultFound:
            flash("User not found")
            return redirect(
                url_for('racer_auth.reset_token'))

    return render_template('reset-password.html')


@racer_auth.route(
    "/update-password/<token>", methods=["GET", "POST"], strict_slashes=False)
def save_new_password(token):
    """ The racer reset route handler. """

    if not token:
        flash("Invalid token")
        return redirect(url_for('racer_auth.reset_token'))

    if request.method == 'POST':
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if not password:
            flash("Password is required")
            return redirect(
                url_for('racer_auth.save_new_password', token=token))

        if not confirm_password:
            flash("Confirm Password is required")
            return redirect(
                url_for('racer_auth.save_new_password', token=token))

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(request.referrer)

        try:
            # Check if token exists
            if not valid_token(token):
                flash("Invalid token")
                return redirect(url_for('racer_auth.reset_token', token=token))

            flash("Updating password")
            update_password(token, hash_password(password))
            return redirect(url_for('racer_auth.login'))

        except NoResultFound:
            flash("User not found problem")
            return redirect(url_for('racer_auth.reset_token'))

    return render_template('new-password.html', token=token)
