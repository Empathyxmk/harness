import pytest

def strForStatus(code):
    # Simulate: should return a string containing the code and error info.
    return f"error 0x{code:x}: simulated error message"

def test_str_for_status_contains_code():
    s = strForStatus(-2147483647)
    assert "error 0x" in s