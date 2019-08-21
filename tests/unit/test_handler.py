import pytest

from json import dumps

from functions.release import handler


def test_handler():
    event = {'body': dumps({'action': 'unpublished'})}
    context = None
    response = handler(event, context)
    assert response['statusCode'] == 204
