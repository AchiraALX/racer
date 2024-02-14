#!/usr/bin/env python3


"""Tests for api
"""

import pytest
from app.main import racer


@pytest.fixture()
def app():
    """ App instance """
    racer_app = racer()
    racer_app.config.update({
        "TESTING": True
    })

    yield racer_app
