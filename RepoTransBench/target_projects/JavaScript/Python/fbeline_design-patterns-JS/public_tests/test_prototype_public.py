class Sheep:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def clone(self):
        return Sheep(self.name, self.weight)

def test_should_clone_with_different_data():
    original = Sheep('Dolly', 60)
    clone = original.clone()
    assert clone is not original
    assert clone.name == 'Dolly'
    assert clone.weight == 60

def test_should_not_mutate_original_after_clone_renamed_different_data():
    sheep = Sheep('Larry', 53)
    clone = sheep.clone()
    clone.name = 'Barry'
    assert sheep.name == 'Larry'
    assert clone.name == 'Barry'