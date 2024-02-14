#!/usr/bin/env python3

""" The racer db tests """


import unittest
from database.database import Database
from database.models.user import User
from database.models.message import Message
from sqlalchemy.exc import IntegrityError


class TestDatabase(unittest.TestCase):
    """ Test db class """

    def test_database_connection(self):
        """ Test db """
        db = Database()
        self.assertIsNotNone(db.engine)

    def test_adding_user(self):
        """If connection succeeds try creating a user

        tests:
            racer_add -> Adding user
            get_user -> Getting user from database
        """

        db = Database()
        _user = User(
            username="achira",
            email='test@email.com',
            password='mypassword'
        )
        try:
            db.racer_add(_user)

        except IntegrityError:
            raise IntegrityError from IntegrityError

        except TypeError:
            return self.assertRaises(TypeError)

        user = db.get_user(email='test@email.com')

        return self.assertTrue(user.email, 'test@email.com')


if __name__ == "__main__":
    unittest.main()
