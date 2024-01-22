#!/usr/bin/env python3

""" The racer db tests """


import unittest
from database import DBStorage


class TestDatabase(unittest.TestCase):
    """ Test db class """

    def test_database(self):
        """ Test db """
        db = DBStorage()
        self.assertIsNotNone(db.engine)


if __name__ == "__main__":
    unittest.main()
