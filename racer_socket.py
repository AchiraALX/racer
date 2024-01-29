#!/usr/bin/env python3


""" Server for multithreaded (asynchronous) chat application. """


import asyncio
import signal
import os
import subprocess
import websockets
from hypercorn.asyncio import serve
from hypercorn.config import Config
from sockets import connect, racer_socket
from workers.rabbit import Broker
from workers.redis import Cache


config = Config()
config.bind = ["localhost:8000"]


async def main():
    """ Server the socket """
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get('PORT', '8001'))

    async with websockets.serve(connect, "", port):
        await stop


def rabbit():
    """ Rabbitmq connection """
    print("Starting server ....")

    rabbit_con = Broker(host='20.62.199.174', port=5672)
    channel = rabbit_con.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    LOG = "logging.getLogger('websockets')"
    channel.basic_publish(exchange='logs', routing_key='', body=LOG)
    print(f" [x] Sent {LOG}")

    channel.close()

    print("Closing server ....")


def redis_main():
    """ Redis connection """
    print("Starting server ....")

    use_local_redis = os.environ.get('USE_LOCAL_REDIS', False)
    if use_local_redis:
        cache = Cache(host='localhost', port=6379)
        rabbit()
        print(cache.ping())
    else:
        subprocess.run(
            ["docker", "run", "--network", "racer_network", "racer"],
            check=True)


if __name__ == '__main__':
    print("Starting server ....")

    # Try to run asynchio server and on KeyboardInterrupt prit exited
    try:
        asyncio.run(serve(racer_socket, config))

    except KeyboardInterrupt:
        print("Exited")
