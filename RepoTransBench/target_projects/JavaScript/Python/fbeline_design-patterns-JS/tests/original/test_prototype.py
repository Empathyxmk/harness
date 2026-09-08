import pytest

class Sheep:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def clone(self):
        return Sheep(self.name, self.weight)

def test_should_clone():
    original = Sheep('Original', 75)
    clone = original.clone()
    assert clone is not original
    assert clone.name == 'Original'
    assert clone.weight == 75

def test_should_not_mutate_original_after_clone_renamed():
    sheep = Sheep('Henry', 40)
    clone = sheep.clone()
    clone.name = 'Not Henry'
    assert sheep.name == 'Henry'
    assert clone.name == 'Not Henry'