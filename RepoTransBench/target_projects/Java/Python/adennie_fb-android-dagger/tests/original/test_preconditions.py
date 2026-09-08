import pytest

def check_state(expression, message=None):
    if not expression:
        if message is not None:
            raise IllegalStateException(message)
        else:
            raise IllegalStateException()

class IllegalStateException(Exception):
    pass

def test_check_state_true_condition():
    check_state(True, "Should not raise.")

def test_check_state_false_condition():
    with pytest.raises(IllegalStateException):
        check_state(False, "This is an error message.")

def test_check_state_false_condition_with_message():
    try:
        check_state(False, "Custom error message")
        assert False, "Expected IllegalStateException not thrown"
    except IllegalStateException as e:
        assert str(e) == "Custom error message"