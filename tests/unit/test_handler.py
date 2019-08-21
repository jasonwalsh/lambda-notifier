import pytest

from json import load
from os import path

from functions.release import handler


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))


@pytest.fixture
def event():
    """Represents an Amazon API Gateway event"""
    with open(path.join(BASE_DIR, '..', 'event.json')) as f:
        return load(f)


def test_handler(event):
    context = None
    response = handler(event, context)
    assert response['statusCode'] == 200
