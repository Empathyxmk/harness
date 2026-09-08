import pytest
from enum import Enum

class Animal(Enum):
    CAT = 0
    DOG = 1
    BIRD = 2

    @classmethod
    def _from_string(cls, name):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(f"No such enum value: {name}")

    @classmethod
    def _from_string_nothrow(cls, name):
        try:
            return cls[name]
        except KeyError:
            return None

    @classmethod
    def _values(cls):
        return list(cls)

    def _to_string(self):
        return self.name

def test_enum_name():
    a_cat = Animal.CAT
    a_dog = Animal.DOG
    a_bird = Animal.BIRD

    assert a_cat._to_string() == "CAT"
    assert a_dog._to_string() == "DOG"
    assert a_bird._to_string() == "BIRD"

def test_enum_from_string():
    a1 = Animal._from_string("DOG")
    assert a1 == Animal(Animal.DOG)

    a2 = Animal._from_string_nothrow("BIRD")
    assert a2 is not None and a2 == Animal(Animal.BIRD)

    a3 = Animal._from_string_nothrow("NOT_AN_ANIMAL")
    assert a3 is None  # Should be None/False

def test_enum_value():
    assert Animal.CAT.value == 0
    assert Animal.DOG.value == 1
    assert Animal.BIRD.value == 2

def test_enum_iteration():
    count = 0
    for e in Animal._values():
        _ = e
        count += 1
    assert count == 3