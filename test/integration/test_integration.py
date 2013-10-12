import os
import json
import subprocess
import tempfile
import time

from nose.tools import eq_, raises

import btsync


CONFIG = {
    "device_name": "MY TESTING NODE",
    "listening_port": 0,
    "storage_path": "",
    "webui":
    {
        "listen": "0.0.0.0:8888",
        "login": "admin",
        "password": "password"
    }
}


BTSYNC_EXECUTABLE = os.environ.get('BTSYNC', 'btsync')
PORT = os.environ.get('BTSYNC_PORT', 59999)


class TestIntegration(object):
    def setup(self):
        storage_path = tempfile.mkdtemp()

        _, config_file_name = tempfile.mkstemp()

        with open(config_file_name, 'w') as f:
            CONFIG['storage_path'] = storage_path
            CONFIG['webui']['listen'] = '0.0.0.0:%s' % PORT
            json.dump(CONFIG, f)

        self.btsync_process = subprocess.Popen([
            BTSYNC_EXECUTABLE, '--nodaemon',
            '--config', config_file_name,
        ], stdout=open('/dev/null'))
        time.sleep(0.5)

        self.client = btsync.Client(
            host='127.0.0.1',
            port=PORT,
            username='admin',
            password='password',
        )

    def teardown(self):
        self.btsync_process.kill()

    def test_add_sync_folder_readonly(self):
        readonly_secret = self.client.generate_secret()['rosecret']
        folder_name = tempfile.mkdtemp()
        self.client.add_sync_folder(folder_name, readonly_secret)
        sync_folders = self.client.sync_folders
        eq_(1, len(sync_folders))
        eq_(folder_name, sync_folders[0]['name'])
        eq_(readonly_secret, sync_folders[0]['secret'])
        eq_(0, sync_folders[0]['iswritable'])

    def test_add_sync_folder_readwrite(self):
        secret = self.client.generate_secret()['secret']
        folder_name = tempfile.mkdtemp()
        self.client.add_sync_folder(folder_name, secret)
        sync_folders = self.client.sync_folders
        eq_(1, len(sync_folders))
        eq_(folder_name, sync_folders[0]['name'])
        eq_(secret, sync_folders[0]['secret'])
        eq_(1, sync_folders[0]['iswritable'])

    @raises(btsync.BtsyncException)
    def test_add_sync_folder_folder_already_exists(self):
        secret = self.client.generate_secret()['secret']
        folder_name = tempfile.mkdtemp()
        self.client.add_sync_folder(folder_name, secret)
        eq_(1, len(self.client.sync_folders))
        self.client.add_sync_folder(folder_name, secret)

    def test_remove_sync_folder(self):
        secret = self.client.generate_secret()['secret']
        folder_name = tempfile.mkdtemp()
        self.client.add_sync_folder(folder_name, secret)
        eq_(1, len(self.client.sync_folders))

        self.client.remove_sync_folder(folder_name, secret)
        eq_(0, len(self.client.sync_folders))

    def test_get_settings(self):
        keys = set([
            'dlrate', 'devicename', 'ulrate',
            'portmapping', 'listeningport',
        ])
        eq_(keys, set(self.client.settings.keys()))

    def test_set_settings(self):
        yield self._assert_settings, 'dlrate', 99
        yield self._assert_settings, 'devicename', 'FOOBAR'
        yield self._assert_settings, 'ulrate', 88
        yield self._assert_settings, 'portmapping', 0
        yield self._assert_settings, 'listeningport', 65535

    def _assert_settings(self, key, value):
        settings = self.client.settings
        settings[key] = value
        self.client.set_settings(settings)
        new_settings = self.client.settings
        eq_(value, new_settings[key])

    def test_set_folder_preference(self):
        for flag in (0, 1):
            yield self._assert_set_folder_preference, 'deletetotrash', flag
            yield self._assert_set_folder_preference, 'relay', flag
            yield self._assert_set_folder_preference, 'searchdht', flag
            yield self._assert_set_folder_preference, 'searchlan', flag
            yield self._assert_set_folder_preference, 'usehosts', flag
            yield self._assert_set_folder_preference, 'usetracker', flag

    def _assert_set_folder_preference(self, key, value):
        secret = self.client.generate_secret()['secret']
        folder_name = tempfile.mkdtemp()
        self.client.add_sync_folder(folder_name, secret)
        preference = self.client.get_folder_preference(folder_name, secret)
        preference[key] = value
        self.client.set_folder_preference(folder_name, secret, preference)
        new_pref = self.client.get_folder_preference(folder_name, secret)
        eq_(value, new_pref[key])
