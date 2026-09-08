import pytest

def test_check_not_null_non_null_public():
    def check_not_null(val):
        if val is None:
            raise NullPointerException()
        return val
    class NullPointerException(Exception): pass
    s = "not null"
    assert check_not_null(s) is s

def test_check_not_null_null_public():
    def check_not_null(val):
        if val is None:
            raise NullPointerException()
        return val
    class NullPointerException(Exception): pass
    with pytest.raises(NullPointerException):
        check_not_null(None)