import pytest

class Preconditions:
    @staticmethod
    def check_not_null(obj, msg=None):
        if obj is None:
            raise NullPointerException(msg or "Object is null")
        return obj

    @staticmethod
    def check_state(expression, msg=None):
        if not expression:
            raise IllegalStateException(msg or "")

class NullPointerException(Exception):
    pass

class IllegalStateException(Exception):
    pass

def test_check_not_null_not_null_public():
    my_string = "notNullPublic"
    Preconditions.check_not_null(my_string, "Must not be null")
    Preconditions.check_not_null(my_string)
    Preconditions.check_not_null(5)

def test_check_not_null_null_public():
    with pytest.raises(NullPointerException):
        Preconditions.check_not_null(None, "Error: is null")

def test_check_state_true_public():
    Preconditions.check_state(2 > 1, "True expected")
    Preconditions.check_state(True)

def test_check_state_false_public():
    with pytest.raises(IllegalStateException):
        Preconditions.check_state(3 < 1, "Should fail")