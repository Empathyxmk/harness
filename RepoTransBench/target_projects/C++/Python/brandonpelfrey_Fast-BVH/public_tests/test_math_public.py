import pytest
import math
from fastbvh.vector3 import Vector3

@pytest.mark.parametrize("T", [float, float])
class TestVector3Public:  # C++ ran float,double, but using float only in Python for simplicity
    def test_ComparisonOperatorsPublic(self, T):
        a = Vector3(T(7), T(8), T(9))
        b = Vector3(T(7), T(8), T(9))
        c = Vector3(T(8), T(8), T(9))
        assert a == b
        assert not (a == c)
        assert a != c

    def test_AdditionAndSubtractionPublic(self, T):
        v1 = Vector3(T(10), T(20), T(30))
        v2 = Vector3(T(-7), T(5), T(3))
        s = v1 + v2
        assert math.isclose(s.x, T(3))
        assert math.isclose(s.y, T(25))
        assert math.isclose(s.z, T(33))
        d = v1 - v2
        assert math.isclose(d.x, T(17))
        assert math.isclose(d.y, T(15))
        assert math.isclose(d.z, T(27))

    def test_ScalarMultiplicationAndDivisionPublic(self, T):
        v = Vector3(T(-6), T(9), T(12))
        v2 = v * T(3)
        assert math.isclose(v2.x, T(-18))
        assert math.isclose(v2.y, T(27))
        assert math.isclose(v2.z, T(36))
        v3 = v2 / T(9)
        assert math.isclose(v3.x, T(-2))
        assert math.isclose(v3.y, T(3))
        assert math.isclose(v3.z, T(4))

    def test_CompoundAssignmentOperatorsPublic(self, T):
        v1 = Vector3(T(2), T(3), T(4))
        v2 = Vector3(T(7), T(-1), T(1))
        v1 = v1 + v2
        assert math.isclose(v1.x, T(9))
        assert math.isclose(v1.y, T(2))
        assert math.isclose(v1.z, T(5))
        v1 = v1 - v2
        assert math.isclose(v1.x, T(2))
        assert math.isclose(v1.y, T(3))
        assert math.isclose(v1.z, T(4))
        v1 = v1 * T(-2)
        assert math.isclose(v1.x, T(-4))
        assert math.isclose(v1.y, T(-6))
        assert math.isclose(v1.z, T(-8))
        v1 = v1 / T(2)
        assert math.isclose(v1.x, T(-2))
        assert math.isclose(v1.y, T(-3))
        assert math.isclose(v1.z, T(-4))

    def test_DotProductPublic(self, T):
        v1 = Vector3(T(2), T(-3), T(5))
        v2 = Vector3(T(-1), T(4), T(7))
        dot_result = v1.dot(v2)
        result = T(2)*T(-1) + T(-3)*T(4) + T(5)*T(7)
        assert math.isclose(dot_result, result)

    def test_MagnitudeAndNormalizePublic(self, T):
        v = Vector3(T(3), T(-4), T(0))
        mag = math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)
        assert math.isclose(v.Length(), mag)
        norm = v.Normalized()
        assert math.isclose(norm.x, T(3.0)/5.0, abs_tol=1e-5)
        assert math.isclose(norm.y, T(-4.0)/5.0, abs_tol=1e-5)
        assert math.isclose(norm.z, T(0.0), abs_tol=1e-5)

    def test_CrossProductPublic(self, T):
        v1 = Vector3(T(0), T(2), T(0))
        v2 = Vector3(T(3), T(0), T(1))
        cross = v1.cross(v2)
        assert math.isclose(cross.x, T(2*1-0*0))
        assert math.isclose(cross.y, T(0*3-0*1))
        assert math.isclose(cross.z, T(0*0-2*3))
        v3 = Vector3(T(-1), T(4), T(-3))
        v4 = Vector3(T(5), T(0), T(2))
        cross2 = v3.cross(v4)
        assert math.isclose(cross2.x, T(4*2-(-3)*0))
        assert math.isclose(cross2.y, T((-3)*5-(-1)*2))
        assert math.isclose(cross2.z, T((-1)*0-4*5))