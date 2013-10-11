from nose.tools import eq_, raises

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
            FIELDS = (
                ('a', int),
                ('b', int),
                ('c', int),
            )

        FooModel(a=1, b=2, c=3, d=4)

    def test_params_have_the_correct_type(self):
        class FooModel(Model):
            FIELDS = (
                ('a', int),
                ('b', str),
            )

        foo = FooModel(a=1, b='2')
        eq_(1, foo['a'])
        eq_('2', foo['b'])
