import pytest
from src import index
from src.cat import Cat
from src.dog import Dog

def test_bundle_exports_cat_and_dog():
    assert getattr(index, "Cat") is Cat
    assert getattr(index, "Dog") is Dog

def test_instantiate_cat_and_dog_via_bundle():
    c = index.Cat()
    d = index.Dog()
    assert c.name == "Cat"
    assert d.name == "Dog"