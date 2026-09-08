import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import jsons

class Animal(jsons.JsonSerializable):
    def __init__(self, species, age):
        self.species = species
        self.age = age

def test_jsonserializable_dump_public():
    a = Animal('cat', 4)
    assert jsons.dump(a) == {'species': 'cat', 'age': 4}

def test_jsonserializable_load_public():
    obj = jsons.load({'species': 'dog', 'age': 10}, Animal)
    assert obj.species == 'dog' and obj.age == 10