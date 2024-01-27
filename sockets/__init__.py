#!/usr/bin/env python3

""" Socket implementation for racer."""

import json
import secrets
from typing import Dict, Any, Optional
import redis
import pika  # type: ignore
from quart import Quart, websocket


REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Global variables
connected_clients: Dict[Any, Any] = {}
connected_hosts: Dict[Any, Any] = {}

# Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
redis_client.ping()


# Rabbitmq connection
rabbit_con = pika.BlockingConnection(
    pika.ConnectionParameters(host='20.127.195.22', port=5672))
channel = rabbit_con.channel()


racer_socket = Quart(__name__)


@racer_socket.websocket('/')
async def connect():
    """ Connect to the socket """

    con = websocket._get_current_object()  # pylint: disable=protected-access

    try:
        while True:
            message = await websocket.receive_json()

            message_type = message.get('type', None)

            if message_type is None:
                await send_error(con, 'Type not provided')
                continue

            token = message.get('token', None)
            if token is None:
                await send_error(con, 'Token not provided')
                continue

            if message_type == 'connect':
                client = message.get('client', None)
                if client is None:
                    await send_error(con, 'Client not provided')
                    continue

                if client == 'guest':
                    connected_clients[token] = con
                    await con.send_json({
                        'type': 'connect',
                        'message': 'Connected'
                    })
                    continue

                if client == 'host':
                    connected_hosts[token] = con
                    await con.send_json({
                        'type': 'connect',
                        'message': 'Connected'
                    })
                    continue

            if message_type == 'message':
                await con.send_json({
                    'type': 'message',
                    'message': 'Message received'
                })
                continue

    except ConnectionError:
        print("Connection error")
        return


# Send error message
async def send_error(_con, message: str) -> None:
    """ Send error message """
    await _con.send_json({
        'type': 'error',
        'message': message
    })


# Send message to client
async def send_message(token: str, message: dict) -> None:
    """ Send message to client """

    if token in connected_clients:
        con = connected_clients[token]
        await con.send_json(message)


# Send message to host
async def send_message_to_host(token: str, message: dict) -> None:
    """ Send message to host """

    if token in connected_hosts:
        con = connected_hosts[token]
        await con.send_json(message)


# Check client and connect appropriately
async def check_client(_con, message: dict) -> bool:
    """ Filter clients """

    client = message.get('client', None)

    if client is None:
        await send_error(_con, 'Client not provided')
        return False

    proceed = False
    try:
        proceed = await check_token(_con, message)
    except TokenException:
        await send_error(_con, f'Token not provided: {message}')
        return False

    if proceed:
        if client == 'guest':
            connected_clients[message['token']] = _con
            await _con.send_json({
                'type': 'connect',
                'message': 'Connected'
            })
            return True

        if client == 'host':
            connected_hosts[message['token']] = _con
            await _con.send_json({
                'type': 'connect',
                'message': 'Connected'
            })
            return True

        await send_error(_con, 'Client not recognized')

    raise ClientException


# Check token and connect appropriately
async def check_token(_con, message: dict) -> bool:
    """ Filter tokens """

    token = message.get('token', None)

    if token is None:
        await send_error(_con, 'Token not provided')
        return False

    raise TokenException


# Token exception
class TokenException(Exception):
    """ Token exception """


# Client exception
class ClientException(Exception):
    """ Client exception """
