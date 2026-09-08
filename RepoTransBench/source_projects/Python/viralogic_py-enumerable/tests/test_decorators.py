import warnings
import pytest
from py_linq import decorators

def test_deprecated_warning():
    @decorators.deprecated("use something else")
    def old_func(x):
        return x + 1

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        res = old_func(2)
        assert res == 3
        assert any(issubclass(warn.category, DeprecationWarning) for warn in w)