class Particle:
    def __init__(self):
        self.mCurrentX = 0
        self.mCurrentY = 0

class ParticleField:
    def __init__(self, ctx):
        self.ctx = ctx
        self.particles = []
    def set_particles(self, particles):
        self.particles = particles

def test_set_particles_public():
    ctx = None
    field = ParticleField(ctx)
    particles = []
    p = Particle()
    particles.append(p)
    field.set_particles(particles)
    assert field is not None
    assert len(particles) == 1