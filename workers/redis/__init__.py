#!/usr/bin/env python3


""" The race redis module """

from redis import Redis


class Cache:
    """ Racer caching using redis """

    def __init__(self, host: str = 'localhost', port: int = 6379):

        self.cache = Redis(host=host, port=port)

    def ping(self):
        """ Ping the redis connection """

        return self.cache.ping()
