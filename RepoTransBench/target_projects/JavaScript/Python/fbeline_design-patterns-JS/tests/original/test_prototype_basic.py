class Sheep:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def clone(self):
        return Sheep(self.name, self.weight)

def test_sanity():
    sheep = Sheep('dolly', 10.3)
    dolly = sheep.clone()
    assert dolly.name == 'dolly'