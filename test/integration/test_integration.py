import json
import subprocess
import tempfile

from nose.tools import eq_

import btsync


PORT = 37369
CONFIG = {
    "device_name": "MY TESTING NODE",
    "listening_port": 0,
    "storage_path": "",
    "webui":
    {
        "listen": "0.0.0.0:%s" % PORT,
        "login": "admin",
        "password": "password"
    }
}


class TestIntegration(object):
    def setup(self):
        storage_path = tempfile.mkdtemp()
        _, config_file_name = tempfile.mkstemp()

        with open(config_file_name, 'w') as f:
            CONFIG['storage_path'] = storage_path
            json.dump(CONFIG, f)

        self.btsync_process = subprocess.Popen([
            '/home/kevin/btsync/btsync', '--nodaemon',
            '--config', config_file_name,
        ])

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
