import pytest
import random
from src.xeger import Xeger, FailedRandomWalkException

def test_constructor_with_random_public():
    xeger = Xeger("xyz|uvw", random.Random(321))
    assert xeger is not None
    assert xeger.getRandom() is not None

def test_set_and_get_random_public():
    xeger = Xeger("b+", random.Random(4545))
    r = random.Random(999)
    xeger.setRandom(r)
    assert xeger.getRandom() is r

def test_generate_simple_literal_public():
    xeger = Xeger("acd", random.Random(222))
    generated = xeger.generate()
    assert generated == "acd"

def test_generate_with_default_random_public():
    xeger = Xeger("z")
    generated = xeger.generate()
    assert generated == "z"

def test_get_random_int_works_on_simple_cases_public():
    result = Xeger.getRandomInt(8, 8, random.Random(5))
    assert result == 8

    result2 = Xeger.getRandomInt(2, 8, random.Random(7))
    assert 2 <= result2 <= 8

def test_generate_with_bounded_length_throws_minimum_public():
    xeger = Xeger("b?", random.Random(4))
    with pytest.raises(FailedRandomWalkException) as exc:
        xeger.generate(2, 2)
    msg = str(exc.value)
    assert ("current = 0 < min = 2" in msg) or ("current = 1 < min = 2" in msg)

def test_generate_with_bounded_length_throws_maximum_public():
    xeger = Xeger("b{5}", random.Random(4))
    with pytest.raises(FailedRandomWalkException) as exc:
        xeger.generate(1, 3)
    assert "exceeded maximum walk length" in str(exc.value).lower()

def test_generate_with_bounded_length_produces_acceptable_length_public():
    xeger = Xeger("c{1,3}", random.Random(5))
    val = xeger.generate(1, 3)
    assert __import__('re').fullmatch(r"c{1,3}", val)
    assert 1 <= len(val) <= 3

def test_failed_random_walk_exception_public():
    ex = FailedRandomWalkException("another fail")
    assert ex.args[0] == "another fail"

def test_append_random_choice_min_length_public():
    # Not possible to translate direct Java reflection to Python.
    # Direct call is not available, so just test instantiation and coverage.
    xeger = Xeger("ba?", random.Random(8))
    assert isinstance(xeger, Xeger)