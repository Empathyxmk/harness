import math
import pytest

# Simple float3 stub for geometric math
class float3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __sub__(self, o):
        return float3(self.x - o.x, self.y - o.y, self.z - o.z)

    def __add__(self, o):
        return float3(self.x + o.x, self.y + o.y, self.z + o.z)

    def __mul__(self, s):
        return float3(self.x * s, self.y * s, self.z * s)

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y and self.z == o.z

def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z

class quadratic_roots:
    def __init__(self, num, ta, tb):
        self.num = num
        self.ta = ta
        self.tb = tb

    def __bool__(self):
        return self.num != 0

def SolveQuadratic(a, b, c):
    d = b * b - 4.0 * a * c
    if d < 0.0:
        return quadratic_roots(0, 0.0, 0.0)
    sqd = math.sqrt(d)
    if d == 0.0:
        return quadratic_roots(1, (-b - sqd) / (2.0 * a), (-b - sqd) / (2.0 * a))
    return quadratic_roots(2, (-b - sqd) / (2.0 * a), (-b + sqd) / (2.0 * a))

def HitCheckRaySphere(sphereposition, radius, _v0, _v1, impact=None, normal=None):
    dv = _v1 - _v0
    v0 = _v0 - sphereposition
    if radius <= 0.0 or _v0 == _v1:
        return 0
    a = dot(dv, dv)
    b = 2.0 * dot(dv, v0)
    c = dot(v0, v0) - radius * radius
    if c < 0.0:
        return 0
    intersections = SolveQuadratic(a, b, c)
    if not intersections:
        return 0
    result = {'impact': None, 'normal': None}
    if 0.0 <= intersections.ta <= 1.0:
        if impact is not None:
            result['impact'] = _v0 + dv * intersections.ta
        if normal is not None and result['impact'] is not None:
            result['normal'] = result['impact'] - sphereposition
        return 1
    if 0.0 <= intersections.tb <= 1.0:
        if impact is not None:
            result['impact'] = _v0 + dv * intersections.tb
        if normal is not None and result['impact'] is not None:
            result['normal'] = result['impact'] - sphereposition
        return 1
    return 0

def test_SolveQuadratic():
    # No real roots
    roots0 = SolveQuadratic(1, 0, 1)
    assert not roots0
    # One root (discriminant=0)
    roots1 = SolveQuadratic(1, 2, 1)
    assert roots1.num == 1
    assert abs(roots1.ta - -1.0) < 1e-5
    # Two roots
    roots2 = SolveQuadratic(1, 0, -1)
    assert roots2.num == 2
    ta, tb = roots2.ta, roots2.tb
    assert (abs(ta - -1.0) < 1e-5 and abs(tb - 1.0) < 1e-5) or (abs(ta - 1.0) < 1e-5 and abs(tb - -1.0) < 1e-5)

def test_HitCheckRaySphere():
    center = float3(0, 0, 0)
    v0 = float3(2, 0, 0)
    v1 = float3(-2, 0, 0)
    impact = float3()
    normal = float3()
    # Normal intersection
    ret = HitCheckRaySphere(center, 1.0, v0, v1, impact, normal)
    assert ret == 1
    # Starts inside sphere (should return 0)
    in0 = float3(0, 0, 0)
    in1 = float3(1, 0, 0)
    ret = HitCheckRaySphere(center, 1.0, in0, in1, impact, normal)
    assert ret == 0
    # No intersection: Ray misses sphere
    far0 = float3(0, 0, 5)
    far1 = float3(0, 2, 5)
    ret = HitCheckRaySphere(center, 1.0, far0, far1, impact, normal)
    assert ret == 0
    # Ray is a point
    ret = HitCheckRaySphere(center, 1.0, v0, v0, impact, normal)
    assert ret == 0
    # Zero radius
    ret = HitCheckRaySphere(center, 0.0, v0, v1, impact, normal)
    assert ret == 0