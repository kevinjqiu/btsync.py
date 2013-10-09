from mock import call, patch, Mock
from nose.tools import eq_, raises

import btsync
from responses import ResponseFixtures


fixtures = ResponseFixtures()


class TestClient(object):
    patchers = []

    def _patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        self.patchers.append(patcher)
        return patcher.start()

    def _make_client(self):
        return btsync.Client(
            host='127.0.0.1',
            port='1106',
            username='admin',
            password='password',
        )

    def _mock_token(self, token=u'T'):
        self.get_token = self._patch(
            'btsync.client.Client._get_token', return_value=token)

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

        self.__class__.patchers = []

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
        self._mock_token()
        self._mock_response('get', fixtures.GETOSTYPE)

        client = self._make_client()

        eq_('linux', client.os_type)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=getostype&token=T&t=999')

    def test_get_version(self):
        self._mock_token()
        self._mock_response('get', fixtures.GETVERSION)

        client = self._make_client()

        eq_('121', client.version)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=getversion&token=T&t=999')

    def test_new_version(self):
        self._mock_token()
        self._mock_response('get', fixtures.CHECKNEWVERSION)

        client = self._make_client()

        eq_({'url': '', 'version': 0}, client.new_version)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=checknewversion&token=T&t=999')

    def test_sync_folders(self):
        self._mock_token()
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
        self._mock_token()
        self._mock_response('get', fixtures.GENERATESECRET)

        client = self._make_client()

        secrets = client.generate_secret()
        eq_('SECRET', secrets['secret'])
        eq_('READONLY', secrets['rosecret'])
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=generatesecret&token=T&t=999')

    def test_get_username(self):
        self._mock_token()
        self._mock_response('get', fixtures.GETUSERNAME)

        client = self._make_client()

        eq_('admin', client.username)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?action=getusername&token=T&t=999')

    def test_add_sync_folder_succeeded(self):
        self._mock_token()
        self._mock_response('get', fixtures.ADDSYNCFOLDER_SUCCESS)

        client = self._make_client()

        client.add_sync_folder('/tmp', 'F00BA4')
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/'
            '?action=addsyncfolder&secret=F00BA4&name=%2Ftmp&token=T&t=999')

    @raises(btsync.BtsyncException)
    def test_add_sync_folder_failed(self):
        self._mock_token()
        self._mock_response('get', fixtures.ADDSYNCFOLDER_ERROR)

        client = self._make_client()

        client.add_sync_folder('/tmp', 'F00BA4')
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?'
            'action=addsyncfolder'
            '&secret=F00BA4'
            '&name=%2Ftmp'
            '&token=T&t=999'
        )

    def test_add_sync_folder_force_succeeded(self):
        self._mock_token()
        self._mock_response('get', fixtures.ADDSYNCFOLDER_SUCCESS)

        client = self._make_client()

        client.add_sync_folder('/tmp', 'F00BA4', force=True)
        self.assert_request_url(
            'http://127.0.0.1:1106/gui/?'
            'force=1'
            '&name=%2Ftmp'
            '&token=T'
            '&secret=F00BA4'
            '&t=999'
            '&action=addsyncfolder'
        )
