from fabric.api import local


def _run_coverage(test_subfolder):
    test_folder = 'test/%s' % test_subfolder
    local('coverage run --source=btsync,%s '
          '$(which nosetests) %s' % (test_folder, test_folder))


def test():
    """Run unit tests"""
    _run_coverage('unit')


def coverage(test_category='unit'):
    """Run tests and show coverage report"""
    assert test_category in ('unit', 'integration')
    if test_category == 'unit':
        test()
    else:
        test_integration()

    local('coverage report -m')


def test_integration():
    """Run integration tests"""
    _run_coverage('integration')
