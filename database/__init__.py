#!/usr/bin/env python3

""" The racer db module """


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

    def racer_add(self, racer: object) -> object:
        """ Add a racer to the database """
        session = self.get_session()
        session.add(racer)
        session.flush()
        session.commit()
        return racer


if __name__ == "__main__":
    db = DBStorage()
    print(db.engine)
