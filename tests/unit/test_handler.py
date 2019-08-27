import os
import pytest

from json import dumps, load, loads
from unittest.mock import Mock, call, create_autospec, patch

from github3.github import GitHub
from jsonschema.exceptions import ValidationError
from functions.client import Client
from functions.aws import handler


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def event():
    """Represents an Amazon API Gateway event"""
    with open(os.path.join(BASE_DIR, '..', 'event.json')) as f:
        return load(f)


@pytest.fixture
def context():
    return None


@pytest.fixture
def session():
    Session = create_autospec(GitHub, spec_set=True)
    return Session(token='4494bc85')


@patch('functions.client.b64decode')
def test_get_file(b64decode, session):
    # The github3.py Repository object
    repository = session.repository
    return_value = Mock(content='SGVsbG8gV29ybGQhCg==')
    repository.return_value.file_contents.return_value = return_value

    client = Client(session)
    client.get_file('octocat/Hello-World', 'README')

    assert repository.call_args == call('octocat', 'Hello-World')
    assert repository.return_value.file_contents.call_args == call('README')
    assert b64decode.call_args == call('SGVsbG8gV29ybGQhCg==')


@patch('functions.aws.validate', autospec=True)
@patch('functions.aws.requests', autospec=True)
@patch('functions.aws.Client', autospec=True)
def test_handler(Client, requests, validate, event, context):
    with open(os.path.join(BASE_DIR, 'unit', 'fixtures', 'schema.json')) as f:
        schema = load(f)

    # The JSON schema used to validate the instance
    requests.get.return_value.json.return_value = schema

    # This instance is not valid according to the JSON schema
    contents = dumps({
        'repositories': [
            'https://github.com/octocat/Hello-World'
        ]
    })

    Client.return_value.get_file.return_value = contents

    # The JSON decoded contents returned from the get_file method
    instance = loads(contents)

    response = handler(event, context)

    assert Client.return_value.get_file.call_args == call(
        'Codertocat/Hello-World', 'deps.json')

    assert validate.call_args == call(instance=instance, schema=schema)

    # Force the validate function to raise a ValidationError
    validate.side_effect = ValidationError(None)

    response = handler(event, context)

    assert response['statusCode'] == 400


def test_invalid_action(context):
    event = {'body': dumps({'action': 'unpublished'})}
    response = handler(event, context)

    assert response['statusCode'] == 204
