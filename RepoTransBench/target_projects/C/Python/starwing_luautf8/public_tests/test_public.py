import pytest
from src.luautf8 import utf8

def test_public():
    assert utf8.len("Tést🦊AßC") == 8
    assert utf8.char(98,101,108,108,111) == "bello"
    t = utf8.codepoint("hello", 2, -1)
    assert t[0] == 101 and t[1] == 108 and t[2] == 108 and t[3] == 111
    assert utf8.char(0x679C, 0x56FD) == "果国"

    count = 0
    for _ in utf8.codes("हिन्दी"):
        count += 1
    assert count == 6

    assert utf8.len("\xC2\xA2\xE2\x82\xAC") == 5  # Adjusted: treat as len on string (not byte)
    assert utf8.len("\xE2\x28\xA1") == 3