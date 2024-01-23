#!/usr/bin/env python3


""" Server for multithreaded (asynchronous) chat application. """


import asyncio
import signal
import os
import websockets
from sockets import connect


async def main():
    """ Server the socket """
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get('PORT', '8001'))

    async with websockets.serve(connect, "", port):
        await stop

if __name__ == "__main__":
    asyncio.run(main())
