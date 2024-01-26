#!/usr/bin/env python3


""" Workers for the racer message broker. """


import pika  # type: ignore


class Broker:
    """ Message broker for racer """

    def __init__(self, host: str = 'localhost', port: int = 5672):
        self.host = host
        self.port = port
        self.connection = None

        if not self.port and self.host:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )

        if not self.port:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self)
            )

        if not self.host:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(port=self.port)
            )

        if self.host and self.port:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port)
            )

    def _connection(self):
        """ Return connection """

        return self.connection

    def channel(self):
        """ Return the channel """
        if self.connection is None:
            return None

        return self.connection.channel()

    def __str__(self):
        return "Make a connection to the rabbitmq-server"
