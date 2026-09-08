from src.company import main
import re

def test_random_string_typical_length():
    s = main.RandomUtil.random_string(5)
    assert s is not None
    assert len(s) == 5
    assert re.match(r'^[A-Za-z0-9]{5}$', s)

def test_random_string_zero_length():
    s = main.RandomUtil.random_string(0)
    assert s is not None
    assert len(s) == 0
    assert s == ""