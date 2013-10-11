class Model(dict):
    def __init__(self, **params):
        assert hasattr(self, 'FIELDS'), "Must define FIELDS"

        for field in self.FIELDS:
            value = params.pop(field)
            self[field] = value

        assert len(params) == 0, "Unrecognized params: %r" % params.keys()


class Settings(Model):
    FIELDS = (
        'dlrate', 'devicename', 'ulrate',
        'portmapping', 'listeningport',
    )
