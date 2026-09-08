import pytest

def test_dummy_public():
    x = 10
    y = 25
    assert x + y == 35

def test_data_structure_public():
    class SimpleThing:
        def __init__(self):
            self.values = [7,9,13]
    thing = SimpleThing()
    assert sum(thing.values) == 29