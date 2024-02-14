#!/usr/bin/env python3

""" The racer db module """
import contextlib
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import DBAPIError, IntegrityError

from .models import Base


class DBStorage:
    """ The racer db class. """

    def __init__(self, drop: bool = False) -> None:
        """ Engine constructor """
        self.engine = create_engine(
            'postgresql://racer:racerpass@localhost/racer'
        )

        if drop:
            Base.metadata.drop_all(self.engine)

        Base.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """ Get a session """
        return self.session()

    def close_session(self) -> None:
        """Close current session
        """

        self.get_session().close()


if __name__ == "__main__":
    db = DBStorage()
    print(db.engine)
