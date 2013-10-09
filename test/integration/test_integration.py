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

BTSYNC_EXECUTABLE = 'btsync'


class TestIntegration(object):
    def setup(self):
        storage_path = tempfile.mkdtemp()

        _, config_file_name = tempfile.mkstemp()

        PORT = 59999
        with open(config_file_name, 'w') as f:
            CONFIG['storage_path'] = storage_path
            CONFIG['webui']['listen'] = '0.0.0.0:%s' % PORT
            json.dump(CONFIG, f)

        self.btsync_process = subprocess.Popen([
            BTSYNC_EXECUTABLE, '--nodaemon',
            '--config', config_file_name,
        ])
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
