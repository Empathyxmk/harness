import pytest
from arduinotrace.trace import strlen

def test_strlen_public():
    assert strlen("!") == 1, "strlen('!') should be 1"
    assert strlen("B") == 1, "strlen('B') should be 1"
    assert strlen("World") == 5, "strlen('World') should be 5"
    assert strlen("Test123") == 7, "strlen('Test123') should be 7"
    assert strlen("abc") == 3, "strlen('abc') should be 3"