#!/usr/bin/env python3


""" The race redis module """

import json
from typing import List
from redis import Redis


class Cache:
    """ Racer caching using redis """

    def __init__(self, host: str = 'localhost', port: int = 6379):

        self.cache = Redis(host=host, port=port)

    def ping(self):
        """ Ping the redis connection """

        return self.cache.ping()

    def retrieve_messages(self, token: str) -> List:
        """ Get messages from redis cache """

        # Select all the messages in cache
        messages = self.cache.keys('*')

        token_messages = []

        for key in messages:  # type: ignore
            message = self.cache.get(key)  # type: ignore
            new_message = json.loads(message)  # type: ignore

            if new_message['frm'] == token or new_message['to'] == token:
                token_messages.append(new_message)

        return token_messages

    def get_all_messages(self):
        """ Get all messages from redis cache """

        # return all messages in the cache
        return self.cache.keys('*')

    # Delete a message from the cache
    def delete_message(self, message_id: str) -> int:
        """ Delete a message from the cache """

        try:
            self.cache.delete(message_id)
            return 1

        except KeyError:
            return 0
