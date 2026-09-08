import re
from src.company import main

def test_random_string_length_one():
    s = main.RandomUtil.random_string(1)
    assert s is not None
    assert len(s) == 1
    assert re.match(r'^[A-Za-z0-9]$', s)

def test_random_string_large_length():
    s = main.RandomUtil.random_string(1000)
    assert s is not None
    assert len(s) == 1000
    assert re.match(r'^[A-Za-z0-9]{1000}$', s)