import os

from json import dumps, load, loads
from unittest.mock import call, patch

from jsonschema.exceptions import ValidationError
from functions.aws import handler

from . import BASE_DIR


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
