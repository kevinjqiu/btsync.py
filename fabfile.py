from fabric.api import local


def _run_coverage_for(kind):
    assert kind in ('unit', 'integration', '')
    test_folder = 'test/{0!s}'.format(kind)
    local('coverage run --source=btsync,%(test_folder)s '
          '$(which nosetests) %(test_folder)s' % dict(
              test_folder=test_folder))


def test():
    """Run unit tests"""
    _run_coverage_for('unit')


def test_all():
    """Run both unit and integration tests"""
    _run_coverage_for('')


def coverage(kind='unit'):
    """Run tests and show coverage report"""
    assert kind in ('unit', 'integration', 'all')
    dict(
        unit=test,
        integration=test_integration,
        all=test_all,
    )[kind]()
    local('coverage report -m')


def test_integration():
    """Run integration tests"""
    _run_coverage_for('integration')
