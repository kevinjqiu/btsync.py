from fabric.api import local


def test():
    """Run unit tests"""
    local('coverage run --source=btsync,test/unit '
          '$(which nosetests) test/unit')


def coverage():
    """Run tests and show coverage report"""
    test()
    local('coverage report -m')


def test_integration():
    """Run integration tests"""
    local('nosetests test/integration')
