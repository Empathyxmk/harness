import pytest
from src.dog import Dog

def test_dog_name_property():
    d = Dog()
    assert d.name == "Dog"