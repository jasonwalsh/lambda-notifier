from json import loads
from unittest.mock import call, patch

from jsonschema.exceptions import ValidationError
from functions.aws import handler

from . import SCHEMA


@patch('functions.aws.validate', autospec=True)
@patch('functions.aws.requests', autospec=True)
@patch('functions.aws.Client', autospec=True)
def test_handler(Client, requests, validate, event, context):
    deps = '{"repositories": ["https://github.com/octocat/Hello-World"]}'
    readme = 'Hello World!'
    Client.with_token.return_value.get_file.side_effect = [deps, readme, deps]

    # The JSON decoded contents returned from the get_file method
    instance = loads(deps)

    requests.get.return_value.json.return_value = SCHEMA

    response = handler(event, context)

    assert validate.call_args == call(instance=instance, schema=SCHEMA)

    assert Client.with_token.return_value.get_file.call_args_list[0] == call(
        'Codertocat/Hello-World', 'deps.json')

    assert Client.with_token.return_value.get_file.call_args_list[1] == call(
        'octocat/Hello-World', 'README')

    assert Client.with_token.return_value.put_file.call_args == call(
        'octocat/Hello-World', 'master', 'Hello World!', 'README',
        'first commit')

    # Force the validate function to raise a ValidationError
    validate.side_effect = ValidationError(None)

    response = handler(event, context)

    assert response['statusCode'] == 400
