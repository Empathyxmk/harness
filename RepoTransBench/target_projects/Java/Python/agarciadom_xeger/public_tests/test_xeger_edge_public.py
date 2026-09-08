import pytest
import random
from src.xeger import Xeger, FailedRandomWalkException

def test_invalid_regex_throws_exception_public():
    with pytest.raises(ValueError):
        # Unclosed parenthesis instead (different from bracket)
        Xeger("(abc", random.Random())

def test_generate_min_equals_max_public():
    generator = Xeger("[cd]{2,2}e", random.Random(77))
    s = generator.generate(3, 3)
    assert len(s) == 3
    assert __import__('re').fullmatch(r"[cd]{2}e", s)

def test_generate_too_short_throws_exception_public():
    generator = Xeger("xyz", random.Random(13))
    with pytest.raises(FailedRandomWalkException):
        generator.generate(5, 5)

def test_generate_accept_on_first_step_public():
    generator = Xeger("b*", random.Random(11))
    s = generator.generate(0, 0)
    assert __import__('re').fullmatch(r"b*", s)
    assert len(s) == 0

def test_generate_normal_flow_public():
    generator = Xeger("abc|xyz", random.Random(3))
    s = generator.generate()
    assert s in ("abc", "xyz")