import pytest

def test_addition_is_correct_public():
    assert 3 + 4 == 7  # 3+4 instead of 2+2

def test_string_equality_public():
    assert "dns66" == "dn" + "s66"