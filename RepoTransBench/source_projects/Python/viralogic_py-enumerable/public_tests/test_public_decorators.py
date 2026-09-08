import warnings
from py_linq import decorators

def test_public_deprecated_warning():
    @decorators.deprecated("please use a new function instead")
    def old_func(x, y=0):
        return x * 2 + y

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = old_func(4, y=3)
        assert res == 11
        assert any(issubclass(warn.category, DeprecationWarning) for warn in w)