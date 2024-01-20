#!/usr/bin/env python3

""" The racer db tests """


import unittest
from db import DBStorage


class TestDB(unittest.TestCase):
    """ Test db class """

    def test_db(self):
        """ Test db """
        db = DBStorage()
        self.assertIsNotNone(db.engine)


