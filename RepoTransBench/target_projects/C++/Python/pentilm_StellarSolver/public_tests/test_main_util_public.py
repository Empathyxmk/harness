import pytest

def add(a, b):
    return a + b

def isNearEqual(a, b, tol=1e-8):
    return abs(a - b) < tol

class Particle:
    def __init__(self):
        self.mass = 0.0

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def addParticle(self, p):
        particle = Particle()
        particle.mass = p.mass
        self.particles.append(particle)

    def getNumParticles(self):
        return len(self.particles)

    def getParticle(self, idx):
        return self.particles[idx]

def test_add_function():
    result = add(12.5, 7.4)
    assert isNearEqual(result, 19.9)

def test_particle_sum_mass():
    sys = ParticleSystem()
    p1 = Particle()
    p2 = Particle()
    p3 = Particle()
    p1.mass = 3.3
    p2.mass = 8.8
    p3.mass = 1.1
    sys.addParticle(p1)
    sys.addParticle(p2)
    sys.addParticle(p3)

    total_mass = 0.0
    for i in range(sys.getNumParticles()):
        total_mass += sys.getParticle(i).mass

    assert isNearEqual(total_mass, 13.2)