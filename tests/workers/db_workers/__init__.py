#!/usr/bin/env python3


"""Test DB workers
"""

import contextlib
import unittest
from faker import Faker
from sqlalchemy.exc import IntegrityError, NoResultFound, DBAPIError
from workers import (
    add_user,
    add_message,
    update_user,
    update_message,
    one_user
)
from database.models.user import User
from database.models.message import Message

fake = Faker()


class TestDbWorkers(unittest.TestCase):
    """Test the workers that interact with the database
    """

    def test_one_user_returns(self):
        """Returning one user
        """
        user = one_user(email="test@email.com")

        self.assertIsNotNone(user)

    def test_one_user_raises(self):
        """
        It should raise NoResultFound
        """

        try:
            one_user(email=fake.email())

        except NoResultFound:
            self.assertRaises(NoResultFound)

    def test_add_user_passes(self):
        """Testing adding a user to db
        """

        username = fake.user_name()
        email = fake.email()
        password = fake.password()

        with contextlib.suppress(IntegrityError):
            add_user({
                "username": username,
                "email": email,
                "password": password
            })

        user = one_user(email=email)
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)

    def test_add_user_fails(self):
        """Given already existing user it should fail
        """

        new_user = {
            "username": "duck",
            "email": "ed127720@students.mu.ac.ke",
            "password": fake.password()
        }

        try:
            add_user(user=new_user)

        except IntegrityError:
            self.assertRaises(IntegrityError)

        except DBAPIError:
            self.assertRaises(DBAPIError)
