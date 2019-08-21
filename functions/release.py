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

    github = GitHub(token=os.getenv('GITHUB_TOKEN'))
    print(github)

    return {
        'statusCode': HTTPStatus.OK
    }
