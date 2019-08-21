import os
import pytest

from json import load
from unittest.mock import call, patch

from functions.release import handler


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def event():
    """Represents an Amazon API Gateway event"""
    with open(os.path.join(BASE_DIR, '..', 'event.json')) as f:
        return load(f)


def test_handler(event):
    context = None
    response = handler(event, context)

    assert response['statusCode'] == 200


@patch('functions.release.get_file', autospec=True)
@patch('functions.release.GitHub', autospec=True)
def test_get_file(client, fn, event):
    context = None
    handler(event, context)

    repository_name = 'Codertocat/Hello-World'
    file_path = 'dependencies.json'
    expected = call(client.return_value, repository_name, file_path)
    actual = fn.call_args

    assert expected == actual
