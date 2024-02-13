#!/usr/bin/env python3


"""Tests for api
"""

import pytest
from app.main import racer


@pytest.fixture()
def app():
    app = racer()
    app.config.update({
        "TESTING": True
    })

    yield app
