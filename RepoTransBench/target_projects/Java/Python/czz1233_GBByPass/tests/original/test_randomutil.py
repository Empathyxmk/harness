import re
from src.company import main

def test_random_string_length():
    assert len(main.RandomUtil.random_string(8)) == 8
    assert len(main.RandomUtil.random_string(1)) == 1
    assert len(main.RandomUtil.random_string(32)) == 32

def test_random_string_characters():
    str_val = main.RandomUtil.random_string(100)
    assert re.match(r'^[A-Za-z0-9]{100}$', str_val)

def test_random_string_zero_and_negative_length():
    assert main.RandomUtil.random_string(0) == ""
    assert main.RandomUtil.random_string(-5) == ""