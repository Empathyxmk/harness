import pytest

def test_public_misc_dummy():
    # Public: Always-True assertion with different fact
    assert 8 < 10

def test_public_misc_other():
    # Public: Reverse a string and check
    assert "XYZ"[::-1] == "ZYX"