from unittest.mock import MagicMock
import pytest

class DummyParticle:
    def __init__(self):
        self.draw_calls = 0
    def draw(self, canvas):
        self.draw_calls += 1

class DummyParticleField:
    def __init__(self, context, attrs=None, style=0):
        self.context = context
        self.attrs = attrs
        self.style = style
        self.particles = []
    def set_particles(self, particles):
        self.particles = particles
    def on_draw(self, canvas):
        for p in self.particles:
            p.draw(canvas)

def test_constructors():
    f1 = DummyParticleField('ctx')
    f2 = DummyParticleField('ctx', 'attrs')
    f3 = DummyParticleField('ctx', 'attrs', 0)
    assert f1.context == 'ctx'
    assert f2.attrs == 'attrs'
    assert f3.style == 0

def test_set_particles_and_on_draw():
    field = DummyParticleField('ctx')
    p1 = DummyParticle()
    p2 = DummyParticle()
    ps = [p1, p2]
    field.set_particles(ps)
    field.on_draw('canvas')
    assert p1.draw_calls >= 1
    assert p2.draw_calls >= 1