import os

from http import HTTPStatus
from json import loads

from github3.github import GitHub


def handler(event, context):
    # ReleaseEvent payload from GitHub
    # https://developer.github.com/v3/activity/events/types/#releaseevent
    body = loads(event['body'])
    action = body['action']

    # Available action types: published, unpublished, created, edited, deleted,
    # or prereleased
    if action != 'published':
        return {
            'statusCode': HTTPStatus.NO_CONTENT
        }

    client = GitHub(token=os.getenv('GITHUB_TOKEN'))

    # For example Codertocat/Hello-World
    repository_name = body['release']['repository']['full_name']
    get_file(client, repository_name, 'dependencies.json')

    return {
        'statusCode': HTTPStatus.OK
    }


def get_file(client, repository_name, file_path):
    pass
