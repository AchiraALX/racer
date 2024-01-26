#!/usr/bin/env python3

""" Socket implementation for racer."""

import json
import secrets
import redis
import pika  # type: ignore

REDIS_HOST = "b8a0e18ed7c2"
REDIS_PORT = 6379

# Global variables
connected_clients = {}
connected_hosts = {}

# Redis client
redis_client = redis.Redis(host='localhost', port=REDIS_PORT)
redis_client.ping()


# Rabbitmq connection
rabbit_con = pika.BlockingConnection(
    pika.ConnectionParameters(host='20.127.195.22', port=5672))
channel = rabbit_con.channel()


# Publish message to rabbitmq
def publish_messages(message: dict) -> None:
    """ Publish message to rabbitmq """

    channel.exchange_declare(exchange='messages', exchange_type='fanout')
    channel.basic_publish(exchange='messages', routing_key='', body=message)
    print(f" [x] Sent {message}")


# Store message to redis
def redis_store_message(message: dict) -> None:
    """ Store message to redis """

    key = secrets.token_hex(16)
    message['id'] = key
    redis_client.set(key, json.dumps(message))
    publish_messages(message)


async def error(websocket, message: str) -> None:
    """ Send error message to websocket client """

    body = {
        'type': 'error',
        'message': message
    }

    await websocket.send(json.dumps(body))


async def add_client(websocket, token: str) -> None:
    """ Add new client to connected_clients """

    if token in connected_clients:
        return
    connected_clients[token] = websocket
    await websocket.send(json.dumps({
        'type': 'connected',
        'message': f'Connected to server on {token}'
    }))


async def add_host(websocket, token: str) -> None:
    """ Add new host to connected_hosts """

    if token in connected_hosts:
        await error(websocket, 'Host already connected')
        return

    connected_hosts[token] = websocket
    print(connected_hosts)
    await websocket.send(json.dumps({
        'type': 'connected',
        'message': f'Connected to server on {token}'
    }))


async def handle_sending(websocket, message: dict) -> None:
    """ Handle message """

    await websocket.send(json.dumps({
        'type': 'message',
        'message': 'Message received'
    }))

    to = message.get('to', None)
    client = message['client']
    if to is None:
        await error(websocket, 'Unknown recipient')
        return

    if client == 'client':
        if to in connected_clients:
            redis_store_message(message)
            await connected_clients[to].send(message)
            return

    elif client == 'host':
        if to in connected_hosts:
            redis_store_message(message)
            await connected_hosts[to].send(message)
            return

    else:
        await error(websocket, "Unable to define the client type")


async def handle_connecting(websocket, message: dict) -> None:
    """ Handle connecting """

    client = message.get('client', None)
    token = message.get('token', None)
    if client is None:
        await error(websocket, 'Unknown client')
        return

    if token is None:
        await error(websocket, 'Unknown token')
        return

    if client == 'client':
        await add_client(websocket, token)
        return

    if client == 'host':
        await add_host(websocket, token)
        return

    await error(websocket, f'Unable to understand the {message}')


# Handle connections
async def connect(websocket):
    """ Handle new websocket connection """

    message = await websocket.recv()
    _message = json.loads(message)

    if _message['type'] == 'connect':
        # Add client to connected_clients and host to connected_hosts

        await handle_connecting(websocket, _message)
        return

    if _message['type'] == 'message':
        # handle the message
        await handle_sending(websocket, _message)
        return

    await error(websocket, 'Unable to dertermine type of message')
