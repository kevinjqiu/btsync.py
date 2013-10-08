import mock
import btsync

from nose.tools import eq_


class TestClient(object):
    @mock.patch('btsync.client._current_timestamp')
    @mock.patch('btsync.client.requests.Session')
    def test_authenticate_should_send_auth_header_and_extract_token(
            self, session_class, current_timestamp):
        current_timestamp.return_value = 100000000
        session_class.return_value = mock_session = mock.Mock()
        TOKEN = \
            u"_0y2dsNVJ_ww1pPcfHxMpro6OLG73jHTWOob9kku9DRLhe-pz_M0a_lHVFIAAAAA"
        mock_session.post.return_value.text = (
            u"<html>"
            u"<div id='token' style='display:none;'>"
            u"{token}"
            u"</div>"
            u"</html>".format(token=TOKEN))

        client = btsync.Client(
            host='127.0.0.1',
            port='1106',
            username='admin',
            password='password',
        )
        eq_(mock_session.auth, ('admin', 'password'))
        eq_(mock_session.post.call_args_list,
            [mock.call('http://127.0.0.1:1106/gui/token.html?t=100000000')])
        eq_(TOKEN, client._token)
