import pytest
import io

class Particle:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.mass = 0.0

class ParticleSystem:
    def __init__(self):
        self.particles = []
    def addParticle(self, p):
        particle = Particle()
        particle.x = p.x
        particle.y = p.y
        particle.mass = p.mass
        self.particles.append(particle)
    def getNumParticles(self):
        return len(self.particles)
    def getParticle(self, idx):
        return self.particles[idx]

def print_particle(p, s):
    s.write(f"{p.x} {p.y} {p.vx} {p.vy} {p.mass}\n")
def print_particle_system(sys, s):
    for i in range(sys.getNumParticles()):
        p = sys.getParticle(i)
        s.write(f"{p.x} {p.y} {p.mass}\n")

def test_print_particle():
    p = Particle()
    p.x = 8.5
    p.y = -1.1
    p.vx = 3.7
    p.vy = -4.2
    p.mass = 6.7

    s = io.StringIO()
    print_particle(p, s)
    output = s.getvalue()
    assert "8.5" in output
    assert "-1.1" in output

def test_print_particle_system():
    system = ParticleSystem()
    p1 = Particle()
    p2 = Particle()
    p1.x = 0.2
    p1.y = 0.4
    p1.mass = 9.0
    p2.x = 6.6
    p2.y = 7.7
    p2.mass = 2.1
    system.addParticle(p1)
    system.addParticle(p2)

    s = io.StringIO()
    print_particle_system(system, s)
    output = s.getvalue()
    assert "0.2" in output
    assert "6.6" in output