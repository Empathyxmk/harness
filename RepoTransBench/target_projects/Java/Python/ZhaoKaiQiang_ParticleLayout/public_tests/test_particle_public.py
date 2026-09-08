class Particle:
    def __init__(self):
        self.mCurrentX = 0.0
        self.mCurrentY = 0.0

def test_initial_values_are_set_public():
    p = Particle()
    p.mCurrentX = 15.0
    p.mCurrentY = 25.0
    assert p.mCurrentX == 15.0
    assert p.mCurrentY == 25.0