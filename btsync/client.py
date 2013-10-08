import requests
import time


def _current_timestamp():
    return int(time.time() * 1000)


class Client(object):
    def __init__(self, **kwargs):
        self._host = kwargs.pop('host')
        self._port = kwargs.pop('port')
        self._username = kwargs.pop('username')
        self._password = kwargs.pop('password')
        self._session = self._authenticate()

    def _extract_token(self, text):
        return (
            text
            .split("<html><div id='token' style='display:none;'>")[1]
            .split("</div></html>")[0]
        )

    def _authenticate(self):
        session = requests.Session()
        session.auth = (self._username, self._password)
        response = session.post('http://{host}:{port}/gui/token.html?t={timestamp}'.format(
            host=self._host, port=self._port, timestamp=_current_timestamp(),
        ))
        response.raise_for_status()
        self._token = self._extract_token(response.text)
        return session
