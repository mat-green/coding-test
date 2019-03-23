# -*- coding: utf-8 -*-

import os
import tempfile

import pytest

from main import create_app


@pytest.fixture
def client():
    flask_app = create_app()
    # Flask provides a way to test your application by exposing the Werkzeug
    # test Client and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


def test_find(client):
    """Finds all stores near TW8 8JN"""

    response = client.get('/find/?postcode=TW8 8JN&radius=20000')
    assert response.status_code == 200
    assert b'TW8 8JW' in response.data
    assert b'Brentford' in response.data
