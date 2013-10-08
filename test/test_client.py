from mock import call, patch, Mock
from nose.tools import eq_

import btsync
from responses import ResponseFixtures


fixtures = ResponseFixtures()


class TestClient(object):
    patchers = []

    def _patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs).start()
        self.patchers.append(patcher)
        return patcher

    def _make_client(self):
        return btsync.Client(
            host='127.0.0.1',
            port='1106',
            username='admin',
            password='password',
        )

    def _mock_token(self, token):
        self.get_token = self._patch('btsync.client.Client._get_token')
        self.get_token.return_value = token

    def _mock_response(self, method, response_text):
        getattr(self.mock_session, method).return_value.text = response_text

    def assert_request_url(self, url, method='get'):
        eq_([call(url)],
            getattr(self.mock_session, method).call_args_list)

    def setup(self):
        self.current_timestamp = self._patch(
            'btsync.client._current_timestamp',
            return_value=999)

        self.mock_session = Mock()
        self.session_class = self._patch(
            'btsync.client.requests.Session',
            return_value=self.mock_session)

    def teardown(self):
        for patcher in self.patchers:
            patcher.stop()

    def test_authenticate_should_send_auth_header_and_extract_token(self):
        TOKEN = \
            u"_0y2dsNVJ_ww1pPcfHxMpro6OLG73jHTWOob9kku9DRLhe-pz_M0a_lHVFIAAAAA"
        self._mock_response(
            'post',
            u"<html>"
            u"<div id='token' style='display:none;'>"
            u"{token}"
            u"</div>"
            u"</html>".format(token=TOKEN))

        client = self._make_client()

        eq_(self.mock_session.auth, ('admin', 'password'))
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/token.html?t=999', method='post')
        eq_(TOKEN, client._token)

    def test_get_os_type(self):
        self._mock_token(u'T')
        self._mock_response('get', fixtures.GETOSTYPE)

        client = self._make_client()

        eq_('linux', client.os_type)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=getostype&token=T&t=999')

    def test_get_version(self):
        self._mock_token(u'T')
        self._mock_response('get', fixtures.GETVERSION)

        client = self._make_client()

        eq_('121', client.version)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=getversion&token=T&t=999')

    def test_new_version(self):
        self._mock_token(u'T')
        self._mock_response('get', fixtures.CHECKNEWVERSION)

        client = self._make_client()

        eq_({'url': '', 'version': 0}, client.new_version)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=checknewversion&token=T&t=999')

    def test_sync_folders(self):
        self._mock_token(u'T')
        self._mock_response('get', fixtures.GETSYNCFOLDERS)

        client = self._make_client()

        eq_([{
            'name': '/home/foo/bar',
            'iswritable': 1,
            'secret': 'A' * 32,
            'size': '353.9 MB in 256 files',
            'peers': [
                {'direct': 1,
                 'name': 'rpi',
                 'status': 'Synced on 10/08/13 11:21:30'
                 }
            ],
            'readonlysecret': 'B' * 32
            }], client.sync_folders)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=getsyncfolders&token=T&t=999')

    def test_generate_secret(self):
        self._mock_token(u'T')
        self._mock_response('get', fixtures.GENERATESECRET)

        client = self._make_client()

        secrets = client.generate_secret()
        eq_('SECRET', secrets['secret'])
        eq_('READONLY', secrets['rosecret'])
        self.assert_request_url('http://127.0.0.1:1106/gui/?action=generatesecret&token=T&t=999')
