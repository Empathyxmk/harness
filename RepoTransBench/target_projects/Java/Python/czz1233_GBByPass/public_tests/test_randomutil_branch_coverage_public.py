from src.company import main
import re

def test_random_string_length_two():
    s = main.RandomUtil.random_string(2)
    assert s is not None
    assert len(s) == 2
    assert re.match(r'^[A-Za-z0-9]{2}$', s)

def test_random_string_medium_length():
    s = main.RandomUtil.random_string(50)
    assert s is not None
    assert len(s) == 50
    assert re.match(r'^[A-Za-z0-9]{50}$', s)