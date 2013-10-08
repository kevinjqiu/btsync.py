import requests


class Client(object):
    def __init__(self, **kwargs):
        self._host = kwargs.pop('host')
        self._port = kwargs.pop('port')
        self._username = kwargs.pop('username')
        self._password = kwargs.pop('password')
        self._session = self._authenticate()

    def _authenticate(self):
        session = requests.Session()
        session.auth = (self._username, self._password)
        session.get('http://{host}:{port}/gui/'.format(
            host=self._host, port=self._port))
        return session
