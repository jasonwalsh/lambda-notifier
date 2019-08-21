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


@patch('functions.release.GitHub', autospec=True)
@patch.dict('os.environ', {'GITHUB_TOKEN': '4cafddbf'})
def test_handler(GitHub, event):
    context = None
    response = handler(event, context)
    assert response['statusCode'] == 200

    assert GitHub.call_count == 1
    assert GitHub.call_args == call(token='4cafddbf')
