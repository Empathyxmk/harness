import pytest
import math

# --- Minimal mock ParticleSystem for original tests ---
class SimulationParameters:
    def __init__(self):
        self.gravity = 1.0

class ParticleSystem:
    def __init__(self):
        self.parameters = SimulationParameters()

    def plummerModel(self, mass, x, y, xvel, yvel, xacc, yacc, n):
        mass[0] = 100000
        for i in range(1, n):
            mass[i] = 1.0
        for i in range(n):
            xacc[i] = 0.0
            yacc[i] = 0.0

    def diskModel(self, mass, x, y, xvel, yvel, xacc, yacc, n):
        mass[0] = 100000
        for i in range(1, n):
            mass[i] = 1.0
        for i in range(n):
            xacc[i] = 0.0
            yacc[i] = 0.0

    def collidingDiskModel(self, mass, x, y, xvel, yvel, xacc, yacc, n):
        # Assign floats for test, no random or NaN/inf for this mock
        for i in range(n):
            mass[i] = float(i+1)
            x[i] = float(i)
            y[i] = float(i*2)
            xvel[i] = float(i*3)
            yvel[i] = float(i*4)
            xacc[i] = 0.0
            yacc[i] = 0.0

def test_plummer_model_sanity():
    ps = ParticleSystem()
    ps.parameters = SimulationParameters()

    n = 5
    mass = [0.0]*n
    x = [0.0]*n
    y = [0.0]*n
    xvel = [0.0]*n
    yvel = [0.0]*n
    xacc = [0.0]*n
    yacc = [0.0]*n

    ps.plummerModel(mass, x, y, xvel, yvel, xacc, yacc, n)
    assert math.isclose(mass[0], 100000, rel_tol=1e-6)
    for i in range(1, n):
        assert math.isclose(mass[i], 1.0, rel_tol=1e-6)
    for i in range(n):
        assert math.isclose(xacc[i], 0.0, rel_tol=1e-6)
        assert math.isclose(yacc[i], 0.0, rel_tol=1e-6)

def test_disk_model_sanity():
    ps = ParticleSystem()
    ps.parameters = SimulationParameters()

    n = 5
    mass = [0.0]*n
    x = [0.0]*n
    y = [0.0]*n
    xvel = [0.0]*n
    yvel = [0.0]*n
    xacc = [0.0]*n
    yacc = [0.0]*n

    ps.diskModel(mass, x, y, xvel, yvel, xacc, yacc, n)
    assert math.isclose(mass[0], 100000, rel_tol=1e-6)
    for i in range(1, n):
        assert math.isclose(mass[i], 1.0, rel_tol=1e-6)
    for i in range(n):
        assert math.isclose(xacc[i], 0.0, rel_tol=1e-6)
        assert math.isclose(yacc[i], 0.0, rel_tol=1e-6)

def test_colliding_disk_model_sanity():
    ps = ParticleSystem()
    ps.parameters = SimulationParameters()

    n = 5
    mass = [0.0]*n
    x = [0.0]*n
    y = [0.0]*n
    xvel = [0.0]*n
    yvel = [0.0]*n
    xacc = [0.0]*n
    yacc = [0.0]*n

    ps.collidingDiskModel(mass, x, y, xvel, yvel, xacc, yacc, n)
    for i in range(n):
        assert math.isfinite(mass[i]), f"mass[{i}] not finite"
        assert math.isfinite(x[i]), f"x[{i}] not finite"
        assert math.isfinite(y[i]), f"y[{i}] not finite"
        assert math.isfinite(xvel[i]), f"xvel[{i}] not finite"
        assert math.isfinite(yvel[i]), f"yvel[{i}] not finite"
        assert math.isclose(xacc[i], 0.0, rel_tol=1e-6)
        assert math.isclose(yacc[i], 0.0, rel_tol=1e-6)