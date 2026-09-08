import pytest
import math
import sys
from fastbvh.vector3 import Vector3
from fastbvh.bbox import BBox

import numpy as np

@pytest.mark.parametrize("T", [float, np.float64, np.float128 if hasattr(np, 'float128') else float])
class TestVector3:
    def test_Constructors(self, T):
        v1 = Vector3(T(0), T(0), T(0))
        assert v1.x == T(0)
        assert v1.y == T(0)
        assert v1.z == T(0)

        v2 = Vector3(T(1), T(2), T(3))
        assert v2.x == T(1)
        assert v2.y == T(2)
        assert v2.z == T(3)

        v3 = Vector3(T(5))
        assert v3.x == T(5)
        assert v3.y == T(5)
        assert v3.z == T(5)

        v4 = Vector3(v2)
        assert v4.x == v2.x
        assert v4.y == v2.y
        assert v4.z == v2.z

    def test_AssignmentOperator(self, T):
        v1 = Vector3(T(1), T(2), T(3))
        v2 = Vector3()
        v2 = Vector3(v1)
        assert v2.x == T(1)
        assert v2.y == T(2)
        assert v2.z == T(3)

    def test_ArithmeticOperators(self, T):
        v1 = Vector3(T(1), T(2), T(3))
        v2 = Vector3(T(4), T(5), T(6))

        add = v1 + v2
        assert add.x == T(5)
        assert add.y == T(7)
        assert add.z == T(9)

        sub = v2 - v1
        assert sub.x == T(3)
        assert sub.y == T(3)
        assert sub.z == T(3)

        mul_scalar = v1 * T(2)
        assert mul_scalar.x == T(2)
        assert mul_scalar.y == T(4)
        assert mul_scalar.z == T(6)

        div_scalar = v2 / T(2)
        assert math.isclose(div_scalar.x, T(2))
        assert math.isclose(div_scalar.y, T(2.5))
        assert math.isclose(div_scalar.z, T(3))

        neg = -v1
        assert neg.x == T(-1)
        assert neg.y == T(-2)
        assert neg.z == T(-3)

    def test_CompoundAssignmentOperators(self, T):
        v1 = Vector3(T(1), T(2), T(3))
        v2 = Vector3(T(4), T(5), T(6))

        v1 = v1 + v2
        assert v1.x == T(5)
        assert v1.y == T(7)
        assert v1.z == T(9)

        v1 = v1 - v2  # back to (1,2,3)
        assert v1.x == T(1)
        assert v1.y == T(2)
        assert v1.z == T(3)

        v1 = v1 * T(2)
        assert v1.x == T(2)
        assert v1.y == T(4)
        assert v1.z == T(6)

        v1 = v1 / T(2)  # back to (1,2,3)
        assert v1.x == T(1)
        assert v1.y == T(2)
        assert v1.z == T(3)

    def test_DotProduct(self, T):
        v1 = Vector3(T(1), T(2), T(3))
        v2 = Vector3(T(4), T(5), T(6))
        assert v1.dot(v2) == T(32)

    def test_CrossProduct(self, T):
        v1 = Vector3(T(1), T(0), T(0))
        v2 = Vector3(T(0), T(1), T(0))
        cross = v1.cross(v2)
        assert cross.x == T(0)
        assert cross.y == T(0)
        assert cross.z == T(1)

        v3 = Vector3(T(1), T(2), T(3))
        v4 = Vector3(T(4), T(5), T(6))
        cross2 = v3.cross(v4)
        assert cross2.x == T(-3)
        assert cross2.y == T(6)
        assert cross2.z == T(-3)

    def test_LengthAndNormalize(self, T):
        v = Vector3(T(3), T(4), T(0))
        EPS = sys.float_info.epsilon if T != np.float128 else np.finfo(np.float128).eps
        assert math.isclose(v.Length(), T(5), abs_tol=EPS)
        assert math.isclose(v.LengthSq(), T(25), abs_tol=EPS)
        normalized = v.Normalized()
        assert math.isclose(normalized.Length(), T(1), abs_tol=EPS*10)

    def test_PerElementMinMax(self, T):
        v1 = Vector3(T(1), T(5), T(3))
        v2 = Vector3(T(4), T(2), T(6))
        min_v = v1.Min(v2)
        assert min_v.x == T(1)
        assert min_v.y == T(2)
        assert min_v.z == T(3)

        max_v = v1.Max(v2)
        assert max_v.x == T(4)
        assert max_v.y == T(5)
        assert max_v.z == T(6)

@pytest.mark.parametrize("T", [float, np.float64, np.float128 if hasattr(np, 'float128') else float])
class TestBBox:
    def test_Constructors(self, T):
        bbox1 = BBox()
        # Default is invalid: pMin.x > pMax.x
        assert bbox1.pMin.x > bbox1.pMax.x

        p1 = Vector3(T(0), T(0), T(0))
        p2 = Vector3(T(1), T(1), T(1))
        bbox2 = BBox(p1, p2)
        assert bbox2.pMin.x == T(0)
        assert bbox2.pMax.x == T(1)

    def test_IsValid(self, T):
        bbox1 = BBox()
        assert not bbox1.IsValid()

        p1 = Vector3(T(0), T(0), T(0))
        p2 = Vector3(T(1), T(1), T(1))
        bbox2 = BBox(p1, p2)
        assert bbox2.IsValid()

    def test_Extent(self, T):
        p1 = Vector3(T(0), T(0), T(0))
        p2 = Vector3(T(10), T(20), T(30))
        bbox = BBox(p1, p2)
        extent = bbox.Extent()
        assert extent.x == T(10)
        assert extent.y == T(20)
        assert extent.z == T(30)

    def test_AddVector(self, T):
        p1 = Vector3(T(0), T(0), T(0))
        p2 = Vector3(T(1), T(1), T(1))
        bbox = BBox(p1, p2)
        add_point = Vector3(T(2), T(-1), T(0.5))
        bbox.Add(add_point)
        assert bbox.pMin.x == T(0)
        assert bbox.pMin.y == T(-1)
        assert bbox.pMin.z == T(0)
        assert bbox.pMax.x == T(2)
        assert bbox.pMax.y == T(1)
        assert bbox.pMax.z == T(1)

    def test_AddBBox(self, T):
        p1 = Vector3(T(0), T(0), T(0))
        p2 = Vector3(T(1), T(1), T(1))
        bbox1 = BBox(p1, p2)
        p3 = Vector3(T(-2), T(0.5), T(2))
        p4 = Vector3(T(0.5), T(3), T(4))
        bbox2 = BBox(p3, p4)
        bbox1.Add(bbox2)
        assert bbox1.pMin.x == T(-2)
        assert bbox1.pMin.y == T(0)
        assert bbox1.pMin.z == T(0)
        assert bbox1.pMax.x == T(1)
        assert bbox1.pMax.y == T(3)
        assert bbox1.pMax.z == T(4)