import pytest
from flaskr.db import get_db


def test_index(client):
    response = client.get('/')
    assert b"Upload" in response.data
    assert b"Lire" in response.data