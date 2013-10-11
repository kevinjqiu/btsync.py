from nose.tools import raises

from btsync.models import Model


class TestModels(object):
    @raises(AssertionError)
    def test_must_define_fields(self):
        class FooModel(Model):  # noqa
            pass

        FooModel()

    @raises(AssertionError)
    def test_must_not_provide_unrecognized_params(self):
        class FooModel(Model):
            FIELDS = ('a', 'b', 'c')

        FooModel(a=1, b=2, c=3, d=4)
