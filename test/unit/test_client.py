from mock import call, patch, Mock
from nose.tools import eq_, raises, assert_raises

import btsync
from responses import ResponseFixtures


fixtures = ResponseFixtures()


def test_unrecognized_params_used_to_construct_client():
    with assert_raises(AssertionError) as e:
        btsync.Client(host='192.168.1.1',
                      port='5555',
                      user='admin',
                      pwd='admin')
    eq_("Unrecognized params: ['pwd', 'user']",
        str(e.exception))


class TestClient(object):
    patchers = []

    HOST = '127.0.0.1'
    PORT = 1106
    USERNAME = 'admin'
    PASSWORD = 'password'

    def _patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        self.patchers.append(patcher)
        return patcher.start()

    def _make_client(self):
        return btsync.Client(
            host=self.HOST,
            port=self.PORT,
            username=self.USERNAME,
            password=self.PASSWORD,
        )

    def _mock_token(self, token=u'T'):
        self.get_token = self._patch(
            'btsync.client.Client._get_token', return_value=token)

    def _mock_response(self, method, response_text):
        getattr(self.mock_session, method).return_value.text = response_text

    def assert_request_url(self, rest_url, method='get'):
        url = 'http://{host}:{port}/gui/{rest_url}'.format(
            host=self.HOST, port=self.PORT, rest_url=rest_url)
        eq_([call(url)],
            getattr(self.mock_session, method).call_args_list)

    def setup(self):
        self.time = self._patch(
            'btsync.client.time.time', return_value=0.999)

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
        self.assert_request_url('token.html?t=999', method='post')
        eq_(TOKEN, client._token)

    def test_get_os_type(self):
        self._mock_token()
        self._mock_response('get', fixtures.GETOSTYPE)

        client = self._make_client()

        eq_('linux', client.os_type)
        self.assert_request_url('?action=getostype&token=T&t=999')

    def test_get_version(self):
        self._mock_token()
        self._mock_response('get', fixtures.GETVERSION)

        client = self._make_client()

        eq_('121', client.version)
        self.assert_request_url('?action=getversion&token=T&t=999')

    def test_new_version(self):
        self._mock_token()
        self._mock_response('get', fixtures.CHECKNEWVERSION)

        client = self._make_client()

        eq_({'url': '', 'version': 0}, client.new_version)
        self.assert_request_url('?action=checknewversion&token=T&t=999')

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
        self.assert_request_url('?action=getsyncfolders&token=T&t=999')

    def test_generate_secret(self):
        self._mock_token()
        self._mock_response('get', fixtures.GENERATESECRET)

        client = self._make_client()

        secrets = client.generate_secret()
        eq_('SECRET', secrets['secret'])
        eq_('READONLY', secrets['rosecret'])
        self.assert_request_url('?action=generatesecret&token=T&t=999')

    def test_get_username(self):
        self._mock_token()
        self._mock_response('get', fixtures.GETUSERNAME)

        client = self._make_client()

        eq_('admin', client.username)
        self.assert_request_url('?action=getusername&token=T&t=999')

    def test_add_sync_folder_succeeded(self):
        self._mock_token()
        self._mock_response('get', fixtures.ADDSYNCFOLDER_SUCCESS)

        client = self._make_client()

        client.add_sync_folder('/tmp', 'F00BA4')
        self.assert_request_url(
            '?action=addsyncfolder&secret=F00BA4&name=%2Ftmp&token=T&t=999')

    @raises(btsync.BtsyncException)
    def test_add_sync_folder_failed(self):
        self._mock_token()
        self._mock_response('get', fixtures.ADDSYNCFOLDER_ERROR)

        client = self._make_client()

        client.add_sync_folder('/tmp', 'F00BA4')

    def test_add_sync_folder_force_succeeded(self):
        self._mock_token()
        self._mock_response('get', fixtures.ADDSYNCFOLDER_SUCCESS)

        client = self._make_client()

        client.add_sync_folder('/tmp', 'F00BA4', force=True)
        self.assert_request_url(
            '?force=1&name=%2Ftmp&token=T&secret=F00BA4'
            '&t=999&action=addsyncfolder')

    def test_remove_sync_folder(self):
        self._mock_token()
        self._mock_response('get', fixtures.REMOVEFOLDER)

        client = self._make_client()

        client.remove_sync_folder('/tmp', 'F00BA4')
        self.assert_request_url(
            '?action=removefolder&secret=F00BA4&name=%2Ftmp&token=T&t=999')

    def test_settings(self):
        self._mock_token()
        self._mock_response('get', fixtures.GETSETTINGS)

        client = self._make_client()

        eq_({
            'devicename': 'MBP',
            'dlrate': 0,
            'listeningport': 58156,
            'portmapping': 1,
            'ulrate': 0
            }, client.settings)
        self.assert_request_url('?action=getsettings&token=T&t=999')

    def test_get_folder_preference(self):
        self._mock_token()
        self._mock_response('get', fixtures.GETFOLDERPREF)

        client = self._make_client()

        eq_({
            "deletetotrash": 1,
            "iswritable": 1,
            "readonlysecret": "READONLY",
            "relay": 1,
            "searchdht": 0,
            "searchlan": 1,
            "usehosts": 0,
            "usetracker": 1
            }, client.get_folder_preference('NAME', 'SECRET'))
        self.assert_request_url(
            '?action=getfolderpref&secret=SECRET&name=NAME&token=T&t=999')

    def test_set_folder_preference(self):
        self._mock_token()
        self._mock_response('get', fixtures.SETFOLDERPREF)

        client = self._make_client()

        client.set_folder_preference('NAME', 'SECRET', {
            'searchlan': 0,
            'usehosts': 0,
            'relay': 1,
            'deletetotrash': 1,
            'iswritable': 1,
            'searchdht': 0,
            'readonlysecret': 'READONLY',
            'usetracker': 0,
        })
        self.assert_request_url(
            '?searchlan=0&name=NAME&relay=1&deletetotrash=1'
            '&iswritable=1&searchdht=0&usehosts=0&secret=SECRET'
            '&t=999&action=setfolderpref&readonlysecret=READONLY'
            '&usetracker=0&token=T')

    def test_generate_invite(self):
        self._mock_token()
        self._mock_response('get', fixtures.GENERATEINVITE)

        client = self._make_client()

        eq_('INVITE_TOKEN', client.generate_invite('NAME', 'SECRET'))
        self.assert_request_url(
            '?action=generateinvite&secret=SECRET&name=NAME&token=T&t=999')

    def test_generate_readonly_invite(self):
        self._mock_token()
        self._mock_response('get', fixtures.GENERATEROINVITE)

        client = self._make_client()

        eq_('READONLY_INVITE_TOKEN',
            client.generate_invite('NAME', 'SECRET', readonly=True))
        self.assert_request_url(
            '?action=generateroinvite&secret=SECRET&name=NAME&token=T&t=999')

    def test_update_secret(self):
        self._mock_token()
        self._mock_response('get', fixtures.UPDATESECRET)

        client = self._make_client()

        client.update_secret('NAME', 'SECRET', 'NEWSECRET')
        self.assert_request_url(
            '?name=NAME&token=T&secret=SECRET&t=999'
            '&action=updatesecret&newsecret=NEWSECRET')

    def test_set_settings(self):
        self._mock_token()
        self._mock_response('get', fixtures.SETSETTINGS)

        client = self._make_client()

        client.set_settings({
            'dlrate': 0,
            'devicename': u'MBP',
            'ulrate': 999,
            'portmapping': 1,
            'listeningport': 58156,
        })
        self.assert_request_url(
            '?dlrate=0&devicename=MBP&token=T'
            '&t=999&listeningport=58156&'
            'action=setsettings&portmapping=1&ulrate=999')
