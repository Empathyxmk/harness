import pytest

class Preconditions:
    def __init__(self):
        raise Exception("This is a utility class and cannot be instantiated.")

    @staticmethod
    def checkNotNull(obj, msg):
        if obj is None:
            raise NullPointerError(msg)
        return obj

class NullPointerError(Exception):
    pass

def test_get_coverage_of_constructor_and_check_constructor_is_private():
    # Test instantiating constructor raises as per Java counterpart
    with pytest.raises(Exception) as e:
        Preconditions()
    assert "utility class" in str(e.value)

def test_check_not_null_given_null_throws_exception():
    with pytest.raises(NullPointerError):
        Preconditions.checkNotNull(None, "message")