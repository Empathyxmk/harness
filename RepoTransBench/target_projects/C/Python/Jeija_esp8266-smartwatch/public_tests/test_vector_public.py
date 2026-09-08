import pytest
import math

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

def test_vector_basic_ops_public():
    a = vector_t(-8.0, 5.0, 2.0)
    b = vector_t(1.0, 4.0, -7.0)
    c = vector_add(a, b)
    assert math.isclose(c.x, -7.0, abs_tol=1e-6)
    assert math.isclose(c.y, 9.0, abs_tol=1e-6)
    assert math.isclose(c.z, -5.0, abs_tol=1e-6)

    c = vector_sub(a, b)
    assert math.isclose(c.x, -9.0, abs_tol=1e-6)
    assert math.isclose(c.y, 1.0, abs_tol=1e-6)
    assert math.isclose(c.z, 9.0, abs_tol=1e-6)

    c = vector_scale(b, 3.0)
    assert math.isclose(c.x, 3.0, abs_tol=1e-6)
    assert math.isclose(c.y, 12.0, abs_tol=1e-6)
    assert math.isclose(c.z, -21.0, abs_tol=1e-6)

    dot = vector_dot(a, b)
    assert math.isclose(dot, -8*1 + 5*4 + 2*-7, abs_tol=1e-6)

    c = vector_cross(a, b)
    assert math.isclose(c.x, 5*-7-2*4, abs_tol=1e-6)
    assert math.isclose(c.y, 2*1-(-8)*-7, abs_tol=1e-6)
    assert math.isclose(c.z, -8*4-5*1, abs_tol=1e-6)

    mag = vector_mag(b)
    assert math.isclose(mag, math.sqrt(1*1+4*4+(-7)*(-7)), abs_tol=1e-6)