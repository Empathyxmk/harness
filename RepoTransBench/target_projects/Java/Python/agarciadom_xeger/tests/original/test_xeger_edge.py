import pytest
import random
from src.xeger import Xeger, FailedRandomWalkException

def test_invalid_regex_throws_exception():
    with pytest.raises(ValueError):
        # Unclosed bracket
        Xeger("[A-Z", random.Random())

def test_generate_min_equals_max():
    gen = Xeger("[ab]{3,3}c", random.Random(42))
    s = gen.generate(4, 4)
    assert len(s) == 4
    assert isinstance(s, str)
    assert __import__('re').fullmatch(r"[ab]{3}c", s)

def test_generate_too_short_throws_exception():
    gen = Xeger("abc", random.Random(42))
    # ask for longer than regex allows to force fail
    with pytest.raises(FailedRandomWalkException):
        gen.generate(4, 4)

def test_generate_accept_on_first_step():
    gen = Xeger("a*", random.Random(42))
    s = gen.generate(0, 0)
    assert __import__('re').fullmatch(r"a*", s)
    assert len(s) == 0

def test_generate_normal_flow():
    gen = Xeger("abc|def", random.Random(1))
    s = gen.generate()
    assert s in ("abc", "def")