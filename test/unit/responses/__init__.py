import os


class ResponseFixtures(object):
    def _path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename + '.json')

    def __getattr__(self, attr):
        with open(self._path(attr.lower())) as f:
            return f.read()
