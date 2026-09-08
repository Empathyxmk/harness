import pytest
import math

# Mock vector_t type and vector math
class vector_t:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    def __eq__(self, other):
        return math.isclose(self.x, other.x, abs_tol=1e-6) and \
               math.isclose(self.y, other.y, abs_tol=1e-6) and \
               math.isclose(self.z, other.z, abs_tol=1e-6)

def vector_add(a, b): return vector_t(a.x + b.x, a.y + b.y, a.z + b.z)
def vector_sub(a, b): return vector_t(a.x - b.x, a.y - b.y, a.z - b.z)
def vector_scale(a, s): return vector_t(a.x*s, a.y*s, a.z*s)
def vector_dot(a, b): return a.x*b.x + a.y*b.y + a.z*b.z
def vector_cross(a, b): return vector_t(
    a.y*b.z - a.z*b.y,
    a.z*b.x - a.x*b.z,
    a.x*b.y - a.y*b.x
)
def vector_mag(a): return math.sqrt(a.x**2 + a.y**2 + a.z**2)

def test_vector_basic_ops():
    a = vector_t(1.0, 2.0, 3.0)
    b = vector_t(4.0, -5.0, 6.0)
    c = vector_add(a, b)
    assert math.isclose(c.x, 5.0, abs_tol=1e-6)
    assert math.isclose(c.y, -3.0, abs_tol=1e-6)
    assert math.isclose(c.z, 9.0, abs_tol=1e-6)

    c = vector_sub(a, b)
    assert math.isclose(c.x, -3.0, abs_tol=1e-6)
    assert math.isclose(c.y, 7.0, abs_tol=1e-6)
    assert math.isclose(c.z, -3.0, abs_tol=1e-6)

    c = vector_scale(a, 2.0)
    assert math.isclose(c.x, 2.0, abs_tol=1e-6)
    assert math.isclose(c.y, 4.0, abs_tol=1e-6)
    assert math.isclose(c.z, 6.0, abs_tol=1e-6)

    dot = vector_dot(a, b)
    assert math.isclose(dot, 1*4 + 2*-5 + 3*6, abs_tol=1e-6)

    c = vector_cross(a, b)
    assert math.isclose(c.x, 2*6-3*-5, abs_tol=1e-6)
    assert math.isclose(c.y, 3*4-1*6, abs_tol=1e-6)
    assert math.isclose(c.z, 1*-5-2*4, abs_tol=1e-6)

    mag = vector_mag(a)
    assert math.isclose(mag, math.sqrt(1*1+2*2+3*3), abs_tol=1e-6)