import pytest

def dummy_function_throw(msg):
    raise RuntimeError("PublicError: " + msg)

def test_throws_runtime_error():
    with pytest.raises(RuntimeError):
        dummy_function_throw("error1")

def test_error_message():
    try:
        dummy_function_throw("errorXYZ")
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "errorXYZ" in str(e)