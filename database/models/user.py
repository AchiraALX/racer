#!/usr/bin/env python3

""" The user model """

from datetime import datetime
from sqlalchemy import (
    String,
    DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from . import Base


class User(Base):
    """ The user class declaration """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(32), nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True
    )

    password: Mapped[str] = mapped_column(
        String(128), nullable=False
    )

    password_reset_token: Mapped[str] = mapped_column(
        String(128), nullable=True
    )

    # Date and time of account creation
    created_at: Mapped[str] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )

    bot_token: Mapped[str] = mapped_column(
        String(100), nullable=True
    )

    def to_dict(self):
        """ Return dictionary representation """

        return {
            "username": self.username,
            "id": self.id,
            "email": self.email,
            "botToken": self.bot_token
        }
