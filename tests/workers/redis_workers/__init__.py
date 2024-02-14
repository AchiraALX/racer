#!/usr/bin/env python3


"""Test workers for redis
"""

from workers.redis import Cache

cache = Cache()


class TestRedisCache:
    """Testing the redis cache
    """

    def test_connection(self):
        """Test the connection to redis
        """
