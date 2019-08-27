from base64 import b64decode


class FileMode:

    NORMAL = '100644'
    EXECUTABLE = '100755'


class Client:

    def __init__(self, session):
        self.session = session

    def create_commit(self, repository_name, branch_name, commit_message,
                      put_files=None):
        """Creates a commit for a repository on the tip of a specified
        branch.
        """
        if put_files is None:
            put_files = []

        repository = self.get_repository(repository_name)

        # For example heads/master
        reference = repository.ref(f'heads/{branch_name}')
        base_tree = repository.tree(reference.object.sha)
        tree = repository.create_tree(put_files, base_tree=base_tree.sha)
        commit = repository.create_commit(
            commit_message, tree.sha, parents=[reference.object.sha])
        reference.update(commit.sha)

    def get_file(self, repository_name, file_path):
        """Returns the base64 decoded contents of a specified file."""
        repository = self.get_repository(repository_name)
        blob = repository.file_contents(file_path)
        return b64decode(blob.content)

    def get_repository(self, repository_name):
        """Returns information about a repository."""
        return self.session.repository(*repository_name.split('/'))

    def put_file(self, repository_name, branch_name, file_content, file_path,
                 commit_message):
        """Adds or updates a file in a branch in a GitHub repository, and
        generates a commit for the addition in the specified branch.
        """
        put_files = [
            {
                'path': file_path,
                'mode': FileMode.NORMAL,
                'type': 'blob',
                'content': file_content
            }
        ]
        self.create_commit(
            repository_name, branch_name, commit_message, put_files=put_files)
