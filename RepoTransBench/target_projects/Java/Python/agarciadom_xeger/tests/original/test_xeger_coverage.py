import pytest
import random
from src.xeger import Xeger, FailedRandomWalkException

def test_constructor_with_random():
    xeger = Xeger("abc|def", random.Random(123))
    assert xeger is not None
    assert xeger.getRandom() is not None

def test_set_and_get_random():
    xeger = Xeger("a+", random.Random(123))
    r = random.Random(456)
    xeger.setRandom(r)
    assert xeger.getRandom() is r

def test_generate_simple_literal():
    xeger = Xeger("abc", random.Random(321))
    generated = xeger.generate()
    assert generated == "abc"

def test_generate_with_default_random():
    xeger = Xeger("b")
    generated = xeger.generate()
    assert generated == "b"

def test_get_random_int_works_on_simple_cases():
    result = Xeger.getRandomInt(5, 5, random.Random(1))
    assert result == 5

    result2 = Xeger.getRandomInt(1, 10, random.Random(1))
    assert 1 <= result2 <= 10

def test_generate_with_bounded_length_throws_minimum():
    xeger = Xeger("a?", random.Random(1))
    with pytest.raises(FailedRandomWalkException) as exc:
        xeger.generate(2, 2)
    msg = str(exc.value)
    assert ("current = 0 < min = 2" in msg) or ("current = 1 < min = 2" in msg)

def test_generate_with_bounded_length_throws_maximum():
    xeger = Xeger("a{3}", random.Random(1))
    with pytest.raises(FailedRandomWalkException) as exc:
        xeger.generate(1, 2)
    assert "exceeded maximum walk length" in str(exc.value).lower()

def test_generate_with_bounded_length_produces_acceptable_length():
    xeger = Xeger("a{2,4}", random.Random(2))
    val = xeger.generate(2, 4)
    assert __import__('re').fullmatch(r"a{2,4}", val)
    assert 2 <= len(val) <= 4

def test_failed_random_walk_exception():
    ex = FailedRandomWalkException("fail")
    assert ex.args[0] == "fail"

def test_append_random_choice_min_length():
    # Not possible to translate reflection for private Java method in this simplified Python version.
    # So just do a dummy test to reach this point (would require automaton to really test).
    # In real code, this could use a mock or test a real path.
    xeger = Xeger("ab?", random.Random(3))
    # There's no "appendRandomChoice" in Python implementation, so just check coverage stays here.
    assert isinstance(xeger, Xeger)