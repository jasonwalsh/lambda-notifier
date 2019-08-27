from unittest.mock import call, patch

from functions.client import Client


def test_create_commit(session):
    client = Client(session)

    # The hash of the HEAD commit
    session.repository.return_value.ref.return_value.object.sha = '553c207'

    # The hash of the base tree
    session.repository.return_value.tree.return_value.sha = '553c207'

    # The hash of the new tree
    session.repository.return_value.create_tree.return_value.sha = '7629413'

    # The objects of the tree structure
    put_files = [
        {
            'path': 'README',
            'mode': '100644',
            'type': 'blob',
            'content': 'Hello World!'
        }
    ]

    client.create_commit(
        'octocat/Hello-World',
        'master',
        'Initial commit',
        put_files=put_files
    )

    assert session.repository.return_value.ref.call_args == call('heads/master')  # noqa
    assert session.repository.return_value.tree.call_args == call('553c207')
    assert session.repository.return_value.create_tree.call_args == call(
        put_files, base_tree='553c207')
    assert session.repository.return_value.create_commit.call_args == call(
        'Initial commit', '7629413', parents=['553c207'])
    assert session.repository.return_value.ref.return_value.update.call_count == 1  # noqa


@patch('functions.client.b64decode')
def test_get_file(b64decode, session):
    session.repository.return_value.file_contents.return_value.content = 'SGVsbG8gV29ybGQhCg=='  # noqa

    client = Client(session)
    client.get_file('octocat/Hello-World', 'README')

    assert session.repository.call_args == call('octocat', 'Hello-World')
    assert session.repository.return_value.file_contents.call_args == call('README')  # noqa
    assert b64decode.call_args == call('SGVsbG8gV29ybGQhCg==')


def test_get_repository(session):
    client = Client(session)
    client.get_repository('octocat/Hello-World')

    assert session.repository.call_args == call('octocat', 'Hello-World')


def test_put_file(session):
    client = Client(session)

    # The hash of the base tree
    session.repository.return_value.tree.return_value.sha = '553c207'

    client.put_file(
        repository_name='octocat/Hello-World',
        branch_name='master',
        file_content='Hello World!',
        file_path='README',
        commit_message='Initial commit'
    )

    put_files = [
        {
            'path': 'README',
            'mode': '100644',
            'type': 'blob',
            'content': 'Hello World!'
        }
    ]

    assert session.repository.return_value.create_tree.call_args == call(
        put_files, base_tree='553c207')
