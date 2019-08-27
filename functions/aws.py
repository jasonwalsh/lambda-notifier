import os
import requests

from http import HTTPStatus
from json import loads

from github3.github import GitHub
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .client import Client


def create_client(token):
    session = GitHub(token=token)
    client = Client(session)
    return client


def handler(event, context):
    body = loads(event['body'])
    if body['action'] != 'published':
        return {
            'statusCode': HTTPStatus.NO_CONTENT
        }

    client = create_client(os.getenv('GITHUB_TOKEN'))
    response = requests.get('https://raw.githubusercontent.com/mongodb-ansible-roles/schemas/master/dependencies.json')  # noqa: E501

    # The JSON schema used to validate the instance
    schema = response.json()

    # For example Codertocat/Hello-World
    repository_name = body['release']['repository']['full_name']

    # The Base64 decoded JSON schema instance
    contents = client.get_file(repository_name, 'deps.json')
    instance = loads(contents)

    try:
        validate(instance=instance, schema=schema)
    except ValidationError:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST
        }
    return {
        'statusCode': HTTPStatus.OK
    }
