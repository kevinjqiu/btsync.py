from fabric.api import local


def test():
    """Run unit tests"""
    local('coverage run --source=btsync,test/unit '
          '$(which nosetests) test/unit')


def coverage(kind):
    """Run tests and show coverage report"""
    assert kind in ('unit', 'integration')
    dict(unit=test, integration=test_integration)[kind]()
    local('coverage report -m')


def test_integration():
    """Run integration tests"""
    local('coverage run --source=btsync,test/integration '
          '$(which nosetests) test/integration')
