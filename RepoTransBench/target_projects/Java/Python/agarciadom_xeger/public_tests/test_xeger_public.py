import re
from src.xeger import Xeger

def test_literal_generation_public():
    regex = "abcXYZ"
    generator = Xeger(regex)
    result = generator.generate()
    assert result == "abcXYZ"

def test_simple_digit_generation_public():
    regex = "[4-6]{4}"
    generator = Xeger(regex)
    result = generator.generate()
    assert len(result) == 4
    assert re.fullmatch(r"[4-6]{4}", result)

def test_simple_alpha_generation_public():
    regex = "[A-C]{3}"
    generator = Xeger(regex)
    result = generator.generate()
    assert len(result) == 3
    assert re.fullmatch(r"[A-C]{3}", result)

def test_range_with_special_char_public():
    regex = "[M-Q]{2}-[7-9]{2}"
    generator = Xeger(regex)
    str_ = generator.generate()
    assert re.fullmatch(r"[M-Q]{2}-[7-9]{2}", str_)

def test_random_numeric_generation_public():
    regex = "[98]{8}"
    generator = Xeger(regex)
    str_ = generator.generate()
    assert len(str_) == 8
    assert re.fullmatch(r"[98]{8}", str_)