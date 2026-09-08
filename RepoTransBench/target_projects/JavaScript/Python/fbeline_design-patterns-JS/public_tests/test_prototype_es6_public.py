class Sheep:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def clone(self):
        return Sheep(self.name, self.weight)

def test_should_clone_with_new_names():
    original = Sheep('Molly', 80)
    clone = original.clone()
    assert clone is not original
    assert clone.name == 'Molly'
    assert clone.weight == 80

def test_renaming_clone_does_not_affect_original_es6_public():
    sheep = Sheep('Bobby', 45)
    clone = sheep.clone()
    clone.name = 'Robbie'
    assert sheep.name == 'Bobby'
    assert clone.name == 'Robbie'