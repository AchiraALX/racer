#!/usr/bin/env python3

""" Race user model """

from secrets import token_hex
from sqlalchemy import String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    """ The Base class fro Racer models """

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=token_hex(16)
    )
