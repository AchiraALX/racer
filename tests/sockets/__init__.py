#!/usr/bin/env python3


"""Testing sockets
"""
import secrets

from sockets import racer_socket

test_client = racer_socket.test_client()
async with test_client.websocket('/') as tst:
    data = {
        "type": "connect",
        "client": "guest",
        "token": secrets.token_urlsafe(16)
    }
    tst.send(data=data)
    result = tst.receive()
