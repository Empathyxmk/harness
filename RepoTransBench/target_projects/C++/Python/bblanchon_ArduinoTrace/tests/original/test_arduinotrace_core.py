import pytest
from arduinotrace.trace import strlen

def test_strlen_core():
    assert strlen("") == 0, "strlen('') should be 0"
    assert strlen("A") == 1, "strlen('A') should be 1"
    assert strlen("Hello") == 5, "strlen('Hello') should be 5"