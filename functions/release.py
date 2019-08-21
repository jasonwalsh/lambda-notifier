from http import HTTPStatus
from json import loads


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
    return {
        'statusCode': HTTPStatus.OK
    }
