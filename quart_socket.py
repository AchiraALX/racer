#!/usr/bin/env python3


""" Racer socket """


import json
from quart import Quart, websocket

app = Quart(__name__)


@app.websocket('/connect')
async def connect():
    """ Connect to the socket """
    while True:
        await websocket.send(json.dumps({'message': 'Hello'}))
        await websocket.receive()


if __name__ == '__main__':
    app.run()
