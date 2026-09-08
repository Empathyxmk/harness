import pytest

def code_with_fatal_error():
    raise RuntimeError("this is fatal")

def code_with_nonfatal_error():
    # In Google Test, non-fatal errors (EXPECT_xx failure) do not raise,
    # but in Python, we can simulate via pytest.fail with a custom marker.
    pytest.fail("this is nonfatal", pytrace=False)

def test_fatal_failure_expect():
    with pytest.raises(RuntimeError, match="this is fatal"):
        code_with_fatal_error()

def test_nonfatal_failure_expect():
    with pytest.raises(pytest.fail.Exception) as excinfo:
        code_with_nonfatal_error()
    # Check the message contains our expected substring:
    assert "nonfatal" in str(excinfo.value)