import pytest
from src.sp import b2b

def test_b2b_flip():
    s = b2b('1011', 4, 4)
    assert isinstance(s, str)
    assert len(s) == 4