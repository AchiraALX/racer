#!/usr/bin/env python3

""" Socket implementation for racer."""

import json


# Global variables
connected_clients = {}
connected_hosts = {}


async def error(websocket, message: str) -> None:
    """ Send error message to websocket client """

    body = {
        'type': 'error',
        'message': message
    }

    await websocket.send_json(body)


async def add_client(websocket, token: str) -> None:
    """ Add new client to connected_clients """

    connected_clients[token] = websocket


async def add_host(websocket, token: str) -> None:
    """ Add new host to connected_hosts """

    connected_hosts[token] = websocket


# Handle connections
async def connect(websocket):
    """ Handle new websocket connection """

    message = await websocket.recv()
    event = json.loads(message)
    assert event['type'] == 'connect'

    # Check if client is already connected
    if event['client_id'] in connected_clients:
        await error(websocket, 'Client already connected')
        return

    # Check if host is already connected
    if event['host_id'] in connected_hosts:
        await error(websocket, 'Host already connected')
        return

    websocket.send_json({'hello': "There my name is"})
