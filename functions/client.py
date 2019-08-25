from base64 import b64decode


class Client:

    def __init__(self, session):
        self.session = session

    def get_file(self, repository_name, file_path):
        """Returns the base-64 decoded contents of a specified file"""
        repository = self.session.repository(*repository_name.split('/'))
        blob = repository.file_contents(file_path)
        return b64decode(blob.content)
