#!/usr/bin/env python3

""" Socket implementation for racer."""

import asyncio
import contextlib
import json
import uuid
from typing import Dict, Any, Optional, List
import redis
import pika  # type: ignore
from quart import Quart, websocket, jsonify
from quart_cors import cors


REDIS_HOST = "localhost"
REDIS_PORT = 6379

RABBITMQ_HOST = '20.127.195.22'

# Global variables
connected_clients: Dict[Any, Any] = {}
connected_hosts: Dict[Any, Any] = {}

# Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
redis_client.ping()


# Rabbitmq connection
rabbit_con = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1', port=5672))
channel = rabbit_con.channel()


racer_socket = Quart(__name__)
cors(racer_socket, allow_origin='*')


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

            client = message.get('client', None)
            if client is None or not client:
                await send_error(con, 'Client not provided')
                continue

            if message_type == 'connect':
                token = message.get('token', None)
                if token is None:
                    await send_error(con, 'Token not provided')
                    continue

                if client == 'guest':
                    connected_clients[token] = con
                    await con.send_json({
                        'type': 'connect',
                        'message': 'Wrong connection for the host'
                    })
                    continue

                if client == 'host':
                    connected_hosts[token] = con
                    await con.send_json({
                        'type': 'connect',
                        'message': 'Received on host message'
                    })
                    continue

            recipient_token = message.get('to', None)
            if recipient_token is None or not recipient_token:
                await send_error(con, "Unknown recipient")
                continue

            src_token = message.get('frm', None)
            if src_token is None or not src_token:
                await send_error(con, 'Unkown client')
                continue

            if message_type == 'message':
                await send_message(con, message)
                continue

    except ConnectionError:
        print("Connection error")
        return

    except asyncio.CancelledError:
        with contextlib.suppress(KeyError):
            del connected_clients[con]
        return


@racer_socket.get('/<host_token>')
async def get_conversations(host_token: str):
    """ Retrieve messages and send them a a json object """

    if host_token is None:
        return jsonify({'error': 'You have to provide a host token'})

    messages = await retrieve_from_redis(host_token=host_token)

    if messages is None:
        return jsonify({'info': "Probaly bad token"})

    else:
        return jsonify({'info': "No messsages or bad token"})

    return jsonify({
        'messages': messages
    })


# Send error message
async def send_error(_con, message: str) -> None:
    """ Send error message """
    await _con.send_json({
        'type': 'error',
        'message': message
    })


# Send message to client
async def send_message(_con, message: dict) -> None:
    """ Send message to client """

    print('Trying to send ..... ')
    print(f'{connected_clients}\n\n{connected_hosts}')
    print(message)

    frm = message['frm']
    to = message['to']
    client = message['client']

    if client == 'host':
        await connected_hosts[frm].send_json(message)
        try:
            await connected_clients[to].send_json(message)

        except KeyError:
            await send_error(
                _con,
                "Not currently connected."
            )

        finally:
            save_message(message)
        return

    if client == 'guest':
        await connected_clients[frm].send_json(message)
        try:
            await connected_hosts[to].send_json(message)

        except KeyError:
            await send_error(
                _con,
                "Host is not currently connected but will leave the message"
            )

        finally:
            save_message(message)

        return

    await send_error(_con, 'Something bad happened.')


# Save message to redis
def save_message(message):
    """ Save the message to the redis server """

    # Only include keys that are serializable
    message = {
        k: v for k, v in message.items() if isinstance(
            k, (str, int, float, type(None)))}

    message_id = str(uuid.uuid4())
    redis_client.set(message_id, json.dumps(message))


# Retrieve messages from the redis server
async def retrieve_from_redis(host_token: str) -> Optional[List]:
    """ Retrieve messages from the the redis server """

    message_keys = redis_client.keys('*')
    host_messages = []

    for key in message_keys:  # type: ignore
        if redis_client.type(key) == b'string':
            message = redis_client.get(key)
            message = json.loads(message)  # type: ignore

            if message['to'] == host_token or message['frm'] == host_token:
                host_messages.append(message)

    return host_messages


# Token exception
class TokenException(Exception):
    """ Token exception """


# Client exception
class ClientException(Exception):
    """ Client exception """


class HostSendingError(Exception):
    """ Raises incase socket is unable to send message to host """


class GuestSendingError(Exception):
    """ Raises incase of error sending messagel to guest """
