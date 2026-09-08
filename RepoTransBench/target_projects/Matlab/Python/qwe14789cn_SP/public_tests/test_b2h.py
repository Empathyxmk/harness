import pytest
from src.sp import b2h

def test_conversion():
    h = b2h('1101', 4)
    assert h == 'D'