#!/usr/bin/env python3

""" The racer db module """
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

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

    @staticmethod
    def close_session(session: Session) -> Optional[None]:
        """Close current session
        """

        session.close()


if __name__ == "__main__":
    db = DBStorage()
    print(db.engine)
