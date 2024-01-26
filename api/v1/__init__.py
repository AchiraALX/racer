#!/usr/bin/env python3


""" Racer API main module """


from flask import Blueprint, request, jsonify


racer_api = Blueprint("racer_api", __name__, url_prefix='/api')


@racer_api.route('/', methods=['GET'], strict_slashes=False)
def ping_api() -> str:
    """ Check live for the API """

    return "pong"
