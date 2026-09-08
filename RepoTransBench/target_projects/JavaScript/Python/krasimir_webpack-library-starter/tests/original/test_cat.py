import pytest
from src.cat import Cat

def test_cat_construct_with_correct_name():
    cat = Cat()
    assert cat.name == "Cat"

def test_cat_access_internal_name_property():
    cat = Cat()
    # Directly testing internal state for completeness
    assert cat._name == "Cat"