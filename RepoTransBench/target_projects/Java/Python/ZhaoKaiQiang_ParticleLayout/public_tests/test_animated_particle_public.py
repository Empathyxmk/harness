class AnimatedParticle:
    def __init__(self):
        self.mLifetime = 0

def test_animated_particle_animation_values_public():
    particle = AnimatedParticle()
    particle.mLifetime = 3000
    assert particle.mLifetime == 3000