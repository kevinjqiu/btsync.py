import requests
import time
import json
import urllib

from btsync.models import Settings, Folder, FolderPreference


def _current_timestamp():
    return int(time.time() * 1000)


class BtsyncException(StandardError):
    def __init__(self, error):
        self.error = error
        self.code = error['error']
        self.message = error['message']

    def __str__(self):
        return self.message


class Client(object):
    """
    Client
    ~~~~~~

    The client that talks to the hosted btsync instance.
    """
    def __init__(self, **kwargs):
        """Constructor

        :params host: the host of the btsync instance to talk to
        :param port: the port of the btsync instance to talk to
        :param username: the admin username for the btsync instance
        :param password: the admin password for the btsync instance
        """
        self._host = kwargs.pop('host', '127.0.0.1')
        self._port = kwargs.pop('port', '8888')
        self._username = kwargs.pop('username', 'admin')
        self._password = kwargs.pop('password', 'password')

        assert len(kwargs.keys()) == 0, \
            "Unrecognized params: %r" % kwargs.keys()
        self._session = self._authenticate()

    def _make_request(self, **kwargs):
        endpoint = kwargs.pop('endpoint', '')
        params = kwargs.pop('params', {})
        with_token = kwargs.pop('with_token', True)
        method = kwargs.pop('method', 'get')
        session = kwargs.pop('session', None)
        is_json = kwargs.pop('is_json', True)

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

        if is_json:
            return json.loads(response.text)
        else:
            return response.text

    def _get_token(self, session):
        response_text = self._make_request(
            endpoint='token.html', method='post',
            session=session, with_token=False, is_json=False)
        return (
            response_text
            .split("<html><div id='token' style='display:none;'>")[1]
            .split("</div></html>")[0]
        )

    def _authenticate(self):
        session = requests.Session()
        session.auth = (self._username, self._password)
        self._token = self._get_token(session)
        return session

    @property
    def os_type(self):
        return self._make_request(
            params={'action': 'getostype'}).get('os', None)

    @property
    def version(self):
        return self._make_request(
            params={'action': 'getversion'}).get('version', None)

    @property
    def new_version(self):
        return self._make_request(
            params={'action': 'checknewversion'}).get('version', None)

    @property
    def sync_folders(self):
        folders = self._make_request(
            params={'action': 'getsyncfolders'}).get('folders', [])
        return [
            Folder(**folder) for folder in folders
        ]

    def generate_secret(self):
        return self._make_request(params={'action': 'generatesecret'})

    def add_sync_folder(self, name, secret, force=False):
        params = {'action': 'addsyncfolder',
                  'name': name,
                  'secret': secret}
        if force:
            params['force'] = 1

        result = self._make_request(params=params)
        if result['error']:
            raise BtsyncException(result)

    def remove_sync_folder(self, name, secret):
        self._make_request(params={
            'action': 'removefolder',
            'name': name,
            'secret': secret,
        })

    @property
    def settings(self):
        return Settings(**self._make_request(params={
            'action': 'getsettings',
        })['settings'])

    def set_settings(self, settings):
        params = {
            'action': 'setsettings',
        }
        params.update(settings)
        self._make_request(params=params)

    def get_folder_preference(self, name, secret):
        response = self._make_request(params={
            'action': 'getfolderpref',
            'name': name,
            'secret': secret,
        })
        return FolderPreference(**response['folderpref'])

    def set_folder_preference(self, name, secret, prefs):
        params = {
            'action': 'setfolderpref',
            'name': name,
            'secret': secret,
        }
        params.update(prefs)
        self._make_request(params=params)

    def update_secret(self, name, secret, new_secret):
        self._make_request(params={
            'action': 'updatesecret',
            'name': name,
            'secret': secret,
            'newsecret': new_secret,
        })

    def generate_invite(self, name, secret, readonly=False):
        invite_action = (
            'generateinvite' if not readonly else 'generateroinvite')
        response = self._make_request(params={
            'action': invite_action,
            'name': name,
            'secret': secret,
        })
        return response['invite']

    @property
    def username(self):
        return self._make_request(params={'action': 'getusername'})['username']
