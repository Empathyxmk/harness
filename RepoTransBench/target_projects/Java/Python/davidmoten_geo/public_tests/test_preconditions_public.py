import pytest

class Preconditions:
    @staticmethod
    def checkNotNull(obj, msg):
        if obj is None:
            raise NullPointerError(msg)
        return obj

class NullPointerError(Exception):
    pass

def test_check_not_null_raises_on_none():
    with pytest.raises(NullPointerError):
        Preconditions.checkNotNull(None, "should fail")

def test_check_not_null_returns_value():
    x = Preconditions.checkNotNull(5, "should work")
    assert x == 5