import pytest
from src.dog import Dog

def test_dog_construct_with_correct_name():
    dog = Dog()
    assert dog.name == "Dog"

def test_dog_one_third_static_getter_returns_3():
    # The original JS static getter is Dog.oneThird
    assert Dog.oneThird == 3

def test_dog_access_internal_name_property():
    dog = Dog()
    assert dog._name == "Dog"