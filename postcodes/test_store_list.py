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


def test_empty_db(client):
    """Start with a blank database."""

    response = client.get('/')
    assert response.status_code == 200
    assert b'AL1 2RJ' in response.data
    assert b'-0.341337' in response.data
    assert b'51.741753' in response.data
    assert b'WD6 4PR' in response.data
    assert b'-0.277805' in response.data
    assert b'51.656694' in response.data
