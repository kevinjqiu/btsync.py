import requests
import time
import json


def _current_timestamp():
    return int(time.time() * 1000)


class Client(object):
    def __init__(self, **kwargs):
        self._host = kwargs.pop('host')
        self._port = kwargs.pop('port')
        self._username = kwargs.pop('username')
        self._password = kwargs.pop('password')
        self._session = self._authenticate()

    def _get_token(self, session):
        response = session.post('http://{host}:{port}/gui/token.html?t={timestamp}'.format(
            host=self._host, port=self._port, timestamp=_current_timestamp(),
        ))
        response.raise_for_status()
        return (
            response.text
            .split("<html><div id='token' style='display:none;'>")[1]
            .split("</div></html>")[0]
        )

    def _authenticate(self):
        session = requests.Session()
        session.auth = (self._username, self._password)
        self._token = self._get_token(session)
        return session

    def get_os_type(self):
        response = self._session.get('http://{host}:{port}/gui/?token={token}&action=getostype&t={timestamp}'.format(
            host=self._host, port=self._port, token=self._token, timestamp=_current_timestamp()))
        response.raise_for_status()
        return json.loads(response.text)
