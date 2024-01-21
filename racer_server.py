#!/usr/bin/env python3

""" The racer gunicorn server module. """

from app.main import racer


if __name__ == "__main__":
    racer.run()
