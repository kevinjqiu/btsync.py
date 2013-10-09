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


License
=======

See [license.txt](license.txt)
