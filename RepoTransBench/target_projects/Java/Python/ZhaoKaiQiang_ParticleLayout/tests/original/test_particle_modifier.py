def test_apply_noop():
    class Particle:
        pass
    class ParticleModifier:
        def apply(self, p, ms):
            return
    p = Particle()
    m = ParticleModifier()
    m.apply(p, 10)