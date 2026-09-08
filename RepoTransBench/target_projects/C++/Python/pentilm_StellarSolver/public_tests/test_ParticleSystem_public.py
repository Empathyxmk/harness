import pytest

class Particle:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.mass = 0.0

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def addParticle(self, p):
        self.particles.append(Particle())
        self.particles[-1].x = p.x
        self.particles[-1].y = p.y
        self.particles[-1].mass = p.mass

    def getNumParticles(self):
        return len(self.particles)

    def getParticle(self, idx):
        return self.particles[idx]

    def removeParticle(self, idx):
        del self.particles[idx]

    def clearParticles(self):
        self.particles.clear()

def test_add_particle():
    system = ParticleSystem()
    p1 = Particle()
    p2 = Particle()
    p1.x = 3.3
    p1.y = 4.4
    p1.mass = 1.2
    p2.x = -2.1
    p2.y = 7.8
    p2.mass = 4.3
    system.addParticle(p1)
    system.addParticle(p2)

    assert system.getNumParticles() == 2
    assert abs(system.getParticle(0).x - 3.3) < 1e-8
    assert abs(system.getParticle(1).mass - 4.3) < 1e-8

def test_remove_particle():
    system = ParticleSystem()
    p1 = Particle()
    p2 = Particle()
    p3 = Particle()
    p1.x = 0.5
    p2.x = 1.5
    p3.x = 2.5
    system.addParticle(p1)
    system.addParticle(p2)
    system.addParticle(p3)
    system.removeParticle(1)
    assert system.getNumParticles() == 2
    assert abs(system.getParticle(1).x - 2.5) < 1e-8

def test_clear_particles():
    system = ParticleSystem()
    p = Particle()
    for i in range(10):
        p.x = i * 0.3
        system.addParticle(p)
    system.clearParticles()
    assert system.getNumParticles() == 0