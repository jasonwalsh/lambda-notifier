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
    owner, repo = body['release']['repository']['full_name'].split('/')
    client.repository(owner, repo)

    return {
        'statusCode': HTTPStatus.OK
    }
