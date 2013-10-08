import requests
import time
import json
import urllib


def _current_timestamp():
    return int(time.time() * 1000)


def _make_action_method(action_name, key):
    def getter(self):
        response = self._make_request(
            params={'action': action_name})

        result = json.loads(response.text)
        return result[key]

    return getter


class Client(object):
    def __init__(self, **kwargs):
        self._host = kwargs.pop('host')
        self._port = kwargs.pop('port')
        self._username = kwargs.pop('username')
        self._password = kwargs.pop('password')
        self._session = self._authenticate()

    def _make_request(self, **kwargs):
        endpoint = kwargs.pop('endpoint', '')
        params = kwargs.pop('params', {})
        with_token = kwargs.pop('with_token', True)
        method = kwargs.pop('method', 'get')
        session = kwargs.pop('session', None)

        params['t'] = _current_timestamp()
        if with_token:
            params['token'] = self._token

        url = 'http://{host}:{port}/gui/{endpoint}?{qs}'.format(
            host=self._host,
            port=self._port,
            endpoint=endpoint,
            qs=urllib.urlencode(params),
        )

        method = getattr(
            session if session is not None else self._session, method)
        assert method is not None, 'Invalid method: %s' % method

        response = method(url)
        response.raise_for_status()
        return response

    def _get_token(self, session):
        response = self._make_request(
            endpoint='token.html', method='post',
            session=session, with_token=False)
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

    os_type = property(_make_action_method('getostype', key='os'))

    version = property(_make_action_method('getversion', key='version'))

    new_version = property(
        _make_action_method('checknewversion', key='version'))

    sync_folders = property(
        _make_action_method('getsyncfolders', key='folders'))
