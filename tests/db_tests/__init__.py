#!/usr/bin/env python3

""" The racer db tests """


import unittest
from database import DBStorage
from database.models.user import User
from database.models.message import Message


class TestDatabase(unittest.TestCase):
    """ Test db class """

    def test_database_connection(self):
        """ Test db """
        db = DBStorage()
        self.assertIsNotNone(db.engine)


    def test_adding_user(self):
        """If connection succeeds try creating a user
        """

        db = DBStorage()
        user = User(
            na
        )



if __name__ == "__main__":
    unittest.main()
