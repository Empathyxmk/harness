import re
from src.company import main

def test_random_string_with_zero_length():
    result = main.RandomUtil.random_string(0)
    assert result is not None
    assert len(result) == 0

def test_random_string_with_negative_length():
    result = main.RandomUtil.random_string(-1)
    assert result is not None
    assert len(result) == 0

def test_random_string_with_high_length():
    result = main.RandomUtil.random_string(100)
    assert result is not None
    assert len(result) == 100

def test_random_string_is_alphanumeric():
    result = main.RandomUtil.random_string(20)
    assert re.match(r'^[A-Za-z0-9]+$', result) or result == ""