class Model(dict):
    def __init__(self, **params):
        assert hasattr(self, 'FIELDS'), "Must define FIELDS"

        for field, factory in self.FIELDS:
            if field in params:
                value = params.pop(field)
                self[field] = factory(value)

        assert len(params) == 0, "Unrecognized params: {0!r}".format(params.keys())


class Settings(Model):
    FIELDS = (
        ('dlrate', int),
        ('devicename', str),
        ('ulrate', int),
        ('portmapping', int),
        ('listeningport', int),
    )


class Peer(Model):
    FIELDS = (
        ('direct', int),
        ('name', str),
        ('status', str),
    )


class Folder(Model):
    FIELDS = (
        ('name', str),
        ('iswritable', int),
        ('secret', str),
        ('readonlysecret', str),
        ('size', str),
        ('peers', lambda peers: [Peer(**peer) for peer in peers]),
        ('readonlysecret', str),
        ('secrettype', int),
        ('files', int),
        ('status', str),
        ('last_modified', str),
        ('indexing', bool),
        ('has_key', bool),
        ('error', str),
        ('date_added', str),
    )


class FolderPreference(Model):
    FIELDS = (
        ('deletetotrash', int),
        ("iswritable", int),
        ("readonlysecret", str),
        ("relay", int),
        ("searchdht", int),
        ("searchlan", int),
        ("usehosts", int),
        ("usetracker", int)
    )
