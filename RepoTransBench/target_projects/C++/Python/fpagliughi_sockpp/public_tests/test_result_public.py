import pytest

class Result:
    def __init__(self, value=None):
        if value is None:
            self._ok = False
            self._value = None
            self._error = 1
        elif value >= 0:
            self._ok = True
            self._value = value
            self._error = 0
        else:
            self._ok = False
            self._value = value
            self._error = 1

    def __bool__(self):
        return self._ok

    def value(self):
        return self._value

    def error(self):
        return self._error

def test_result_default_constructed_is_error():
    res_public = Result()
    assert not res_public
    assert res_public.error() != 0

def test_result_constructed_with_positive_value_different():
    res_public = Result(77)
    assert res_public
    assert res_public.value() == 77
    assert res_public.error() == 0

def test_result_constructed_with_explicit_negative_value_different():
    res_public = Result(-99)
    assert not res_public
    assert res_public.value() == -99
    assert res_public.error() != 0