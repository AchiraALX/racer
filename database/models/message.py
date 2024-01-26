#!/usr/bin/env python3


""" Racer message model """

from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from . import Base


class Message(Base):
    """ Message model """

    __tablename__ = 'messages'

    data: Mapped[str] = mapped_column(
        String(255)
    )
    frm: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    to: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    dtime: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default=datetime.now()
    )

    def to_dict(self):
        """ Return the model as a dictionary """
        return {
            'data': self.data,
            'from': self.frm,
            'to': self.to,
            'dtime': self.dtime
        }
