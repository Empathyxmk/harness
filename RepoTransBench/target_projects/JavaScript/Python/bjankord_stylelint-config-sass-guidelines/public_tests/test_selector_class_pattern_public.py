# Public test for selector-class-pattern
import re

def is_valid_class_name(class_name):
    return re.fullmatch(r'[a-z][a-z0-9-]*', class_name) is not None

def test_valid_class_names():
    assert is_valid_class_name("foo-bar1")
    assert is_valid_class_name("test42-item")

def test_invalid_capital_letters():
    assert not is_valid_class_name("FooBar")

def test_invalid_underscores():
    assert not is_valid_class_name("snake_case")

def test_invalid_startswithnumber():
    assert not is_valid_class_name("42start")

def test_invalid_startswithhyphen():
    assert not is_valid_class_name("-prefixed")