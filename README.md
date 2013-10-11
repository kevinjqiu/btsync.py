     ____   ______  _____ __ __  ____     __      ____  __ __ 
    |    \ |      |/ ___/|  |  ||    \   /  ]    |    \|  |  |
    |  o  )|      (   \_ |  |  ||  _  | /  /     |  o  )  |  |
    |     ||_|  |_|\__  ||  ~  ||  |  |/  /      |   _/|  ~  |
    |  O  |  |  |  /  \ ||___, ||  |  /   \_  __ |  |  |___, |
    |     |  |  |  \    ||     ||  |  \     ||  ||  |  |     |
    |_____|  |__|   \___||____/ |__|__|\____||__||__|  |____/ 
                                                          

[![Build Status](https://travis-ci.org/kevinjqiu/btsync.py.png?branch=master)](https://travis-ci.org/kevinjqiu/btsync.py)
[![Coverage Status](https://coveralls.io/repos/kevinjqiu/btsync.py/badge.png?branch=master)](https://coveralls.io/r/kevinjqiu/btsync.py?branch=master)

A Python API client for BitTorrent Sync


Installation
============

Install from [PyPI](https://pypi.python.org):

    pip install btsync.py

Or Install from source:

    git clone git@github.com:kevinjqiu/btsync.py.git
    cd btsync.py
    pip install -r requirements.txt
    python setup.py install

Examples
========

You need to first download [btsync](http://labs.bittorrent.com/experiments/sync/get-started.html) for your platform.  Once it's downloaded, extract it somewhere and generate a sample config file:

    cd /path/to/btsync
    ./btsync --dump-sample-config > config

Change the default config if you wish.  The pieces of config you need for the client to connect are:
- host
- port (listening port)
- username
- password

Run `btsync` with the config:

    ./btsync --config config

With btsync running, now you can connect to it using this library:

Creating a client:

    In [1]: import btsync

    In [2]: client = btsync.Client(
    ...:     host='127.0.0.1',
    ...:     port='1106',
    ...:     username='admin',
    ...:     password='password')

Listing sync folders:

    In [3]: client.sync_folders
    Out[3]:
    [{u'iswritable': 1,
    u'name': u'/home/foo/bar',
    u'peers': [{u'direct': 1,
        u'name': u'rpi',
        u'status': u'Synced on 10/08/13 11:21:30'}],
    u'readonlysecret': u'--------------------------------',
    u'secret': u'--------------------------------',
    u'size': u'353.9 MB in 256 files'},
    {u'iswritable': 1,
    u'name': u'/tmp',
    u'peers': [],
    u'readonlysecret': u'--------------------------------',
    u'secret': u'--------------------------------',
    u'size': u'56.9 kB in 14 files'}]

Generate a secret for adding a sync folder:

    In [7]: secret = client.generate_secret()

    In [8]: secret
    Out[8]:
    {u'rosecret': u'--------------------------------',
    u'secret': u'--------------------------------'}

Add a sync folder:

    In [10]: client.add_sync_folder('/tmp', secret['rosecret'])

    In [11]: client.sync_folders[1]
    Out[11]:
    {u'iswritable': 0,
    u'name': u'/tmp',
    u'peers': [],
    u'secret': u'--------------------------------',
    u'size': u'0 B in 0 files'}


Development
===========

First, you need to setup a virtualenv, as it segregates local dependencies from the system libraries nicely:

    $ virtualenv btsync.py-env

Activate the virtual environment:

    $ cd btsync.py-env
    $ . btsync.py-env/bin/activate

Clone this repo somewhere, e.g., `$HOME/src/btsync.py`:

    $ git clone git@github.com:kevinjqiu/btsync.py.git
    $ cd btsync.py

Install dev dependencies:

    $ pip install -r requirements-dev.txt

Run tests:

    $ fab test

You can also generate the coverage report:

    $ fab coverage

To run integration tests, you need to have `btsync` executable on your `$PATH`:

    $ fab test_integration

Optionally, you can set an environment variable `BTSYNC` before running the test:

    $ BTSYNC=$HOME/btsync/btsync fab test_integration

To run coverage for integration tests:

    $ fab coverage:integration

You can also change the port the btsync instance for integration test runs on (the default port is 59999):

    $ BTSYNC_PORT=55555 fab test_integration

License
=======

See [license.txt](license.txt)
