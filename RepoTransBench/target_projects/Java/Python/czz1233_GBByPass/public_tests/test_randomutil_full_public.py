from src.company import main
import re

def test_random_string_negative_length():
    val = main.RandomUtil.random_string(-7)
    assert val == ""

def test_random_string_all_valid_characters_many():
    val = main.RandomUtil.random_string(32)
    assert val is not None
    assert len(val) == 32
    assert re.match(r"^[A-Za-z0-9]{32}$", val)