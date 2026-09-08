import pytest

def test_check_not_null_throws():
    def check_not_null(val, msg):
        if val is None:
            raise NullPointerException(msg)
        return val
    class NullPointerException(Exception): pass

    with pytest.raises(NullPointerException):
        check_not_null(None, "err")

def test_check_not_null_no_throw():
    def check_not_null(val, msg):
        if val is None:
            raise NullPointerException(msg)
        return val
    class NullPointerException(Exception): pass
    assert check_not_null("a", "err") == "a"

def test_check_argument_throws():
    def check_argument(expr, msg):
        if not expr:
            raise IllegalArgumentException(msg)
        return expr
    class IllegalArgumentException(Exception): pass
    with pytest.raises(IllegalArgumentException):
        check_argument(False, "arg error")

def test_check_argument_no_throw():
    def check_argument(expr, msg):
        if not expr:
            raise IllegalArgumentException(msg)
        return expr
    class IllegalArgumentException(Exception): pass
    assert check_argument(True, "ok arg") is True