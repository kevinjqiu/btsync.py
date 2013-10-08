import mock
import btsync

from nose.tools import eq_


class TestClient(object):
    def test_authenticate_should_send_cred_as_basic_auth_header(self):
        with mock.patch('btsync.client.requests.Session') as session_class:
            session_class.return_value = mock_session = mock.Mock()
            btsync.Client(
                host='127.0.0.1',
                port='1106',
                username='admin',
                password='password',
            )
            eq_(mock_session.auth, ('admin', 'password'))
            eq_(mock_session.get.call_args_list,
                [mock.call('http://127.0.0.1:1106/gui/')])
