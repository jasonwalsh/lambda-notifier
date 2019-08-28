import os
import requests

from http import HTTPStatus
from json import loads

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .client import Client
from .model import ReleaseEventRequest


def handler(event, context):
    body = loads(event['body'])

    request = ReleaseEventRequest.from_json(body)

    # If the event action is not 'published', then do nothing
    if not request.is_publish:
        return {
            'statusCode': HTTPStatus.NO_CONTENT
        }

    client = Client.with_token(os.getenv('GITHUB_TOKEN'))

    # For example Codertocat/Hello-World
    repository_name = request.release.repository.full_name

    # The Base64 decoded JSON schema instance
    contents = client.get_file(repository_name, 'deps.json')

    instance = loads(contents)

    schema = requests.get(os.getenv('SCHEMA_URL')).json()

    try:
        validate(instance=instance, schema=schema)
    except ValidationError:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST
        }

    for repository in instance['repositories']:
        repository_name = repository.split('/', 3)[-1]
        readme = client.get_file(repository_name, 'README')
        client.put_file(
            repository_name, 'master', readme, 'README', 'first commit')

    return {
        'statusCode': HTTPStatus.OK
    }
