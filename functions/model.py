class Release:

    def __init__(self, tag_name='', repository=None):
        self.tag_name = tag_name
        self.repository = repository

    @classmethod
    def from_json(cls, schema):
        tag_name = schema['tag_name']
        repository = Repository.from_json(schema['repository'])
        return cls(tag_name=tag_name, repository=repository)


class Repository:

    def __init__(self, full_name=''):
        self.full_name = full_name

    @classmethod
    def from_json(cls, schema):
        return cls(**schema)


class ReleaseEventRequest:

    def __init__(self, action='', release=None):
        self.action = action
        self.release = release

    @property
    def is_publish(self):
        return self.action == 'published'

    @classmethod
    def from_json(cls, schema):
        action = schema['action']
        release = Release.from_json(schema['release'])
        return cls(action=action, release=release)
