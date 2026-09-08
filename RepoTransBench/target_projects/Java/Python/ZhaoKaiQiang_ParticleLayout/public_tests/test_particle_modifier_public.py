class Particle:
    def __init__(self):
        self.mCurrentY = 0.0

class ParticleModifier:
    def apply(self, particle, ms):
        particle.mCurrentY = 44.0

def test_modify_public():
    m = ParticleModifier()
    p = Particle()
    m.apply(p, 100)
    assert p.mCurrentY == 44.0