#!/usr/bin/env python3


""" Racer API main module """

from typing import Optional
from flask import Blueprint, request, jsonify
from workers.redis import Cache
from workers import get_conversations


racer_api = Blueprint("racer_api", __name__, url_prefix='/api/v1')


@racer_api.route('/', methods=['GET'], strict_slashes=False)
def ping_api() -> str:
    """ Check live for the API """

    return "pong"


@racer_api.get('/conversations/<string:host>')
def get_convo(host: Optional[str]):
    """ Get messages from a server """

    if host is None or not host:
        host = request.args.get('host')

    if host is None or not host:
        return jsonify({"error": "Host is required"}), 400

    cache = Cache()
    messages = [message for message in cache.retrieve_messages(host)]

    return jsonify(
        {"messages": get_conversations(messages)}), 200


@racer_api.get('/conversation/<string:guest>')
def get_conversation(guest: Optional[str]):
    """ Get messages from a server """

    if guest is None or not guest:
        guest = request.args.get('guest')

    if guest is None or not guest:
        return jsonify({"error": "Guest is required"}), 400

    cache = Cache()
    messages = [message for message in cache.retrieve_messages(guest)]

    return jsonify(
        {"messages": messages}), 200
