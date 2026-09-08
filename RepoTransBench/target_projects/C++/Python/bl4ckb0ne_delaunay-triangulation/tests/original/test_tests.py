import math
import pytest
from dt.vector2 import Vector2
from dt.edge import Edge
from dt.triangle import Triangle
from dt.delaunay import Delaunay

class TestVector2BasicOperations:
    def test_constructor_and_access(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(4.0, 5.0)
        assert v1.x == 1.0
        assert v2.y == 5.0

    def test_equality_operator(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(4.0, 5.0)
        v3 = Vector2(1.0, 1.0)
        assert v1 == v3
        assert not (v1 == v2)

    def test_dist2_and_norm2(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(4.0, 5.0)
        assert pytest.approx(v1.dist2(v2), rel=1e-8) == 25.0
        assert pytest.approx(v1.norm2(), rel=1e-8) == 2.0

    def test_dist_specialized(self):
        v1 = Vector2(1.0, 1.0)
        v3 = Vector2(0.0, 0.0)
        assert pytest.approx(v1.dist(v3), rel=1e-8) == math.sqrt(2.0)

    def test_ostream_operator(self):
        v1 = Vector2(1.0, 1.0)
        s = str(v1)
        assert "Point x: 1" in s

class TestEdgeBasicFunctionality:
    def test_construction_and_equality(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(2.0, 2.0)
        e1 = Edge(v1, v2)
        e2 = Edge(v2, v1)
        e3 = Edge(v1, v1)
        assert e1 == e2
        assert not (e1 == e3)

    def test_ostream_operator(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(2.0, 2.0)
        e1 = Edge(v1, v2)
        s = str(e1)
        assert "Edge" in s

class TestTriangleCoreLogic:
    def test_contains_vertex(self):
        v1 = Vector2(0.0, 0.0)
        v2 = Vector2(4.0, 0.0)
        v3 = Vector2(0.0, 3.0)
        tri = Triangle(v1, v2, v3)
        assert tri.containsVertex(v1)
        assert not tri.containsVertex(Vector2(1.0, 1.0))

    def test_circumcircle_contains(self):
        v1 = Vector2(0.0, 0.0)
        v2 = Vector2(4.0, 0.0)
        v3 = Vector2(0.0, 3.0)
        tri = Triangle(v1, v2, v3)
        # Circumcircle center at (2, 1.5), radius 2.5.
        inside = Vector2(2, 2)
        outside = Vector2(5, 5)
        assert tri.circumCircleContains(inside)
        assert not tri.circumCircleContains(outside)

    def test_operator_eq_for_triangles(self):
        v1 = Vector2(0.0, 0.0)
        v2 = Vector2(4.0, 0.0)
        v3 = Vector2(0.0, 3.0)
        tri = Triangle(v1, v2, v3)
        tri2 = Triangle(v1, v2, v3)
        tri3 = Triangle(v3, v2, v1)
        v4 = Vector2(1.0, 1.0)
        tri4 = Triangle(v1, v2, v4)
        assert tri == tri2
        assert tri == tri3
        assert not (tri == tri4)

    def test_ostream_operator(self):
        v1 = Vector2(0.0, 0.0)
        v2 = Vector2(4.0, 0.0)
        v3 = Vector2(0.0, 3.0)
        tri = Triangle(v1, v2, v3)
        s = str(tri)
        assert "Triangle" in s

class TestDelaunayTriangulationAlgorithm:
    def test_basic_triangulation_works_for_minimal_points(self):
        points = [Vector2(0.0, 0.0), Vector2(4.0, 0.0), Vector2(0.0, 3.0)]
        delaunay = Delaunay()
        triangles = delaunay.triangulate(points)
        assert len(triangles) == 1
        verts = delaunay.getVertices()
        assert len(verts) == 3

    def test_edges_are_present(self):
        points = [Vector2(0.0, 0.0), Vector2(4.0, 0.0), Vector2(0.0, 3.0)]
        delaunay = Delaunay()
        delaunay.triangulate(points)
        edges = delaunay.getEdges()
        assert len(edges) == 3

    def test_get_triangles_reference(self):
        points = [Vector2(0.0, 0.0), Vector2(4.0, 0.0), Vector2(0.0, 3.0)]
        delaunay = Delaunay()
        delaunay.triangulate(points)
        tris = delaunay.getTriangles()
        assert len(tris) == 1

class TestDelaunayLargerInput:
    def test_larger_input(self):
        pts = [Vector2(0,0), Vector2(1,0), Vector2(2,0), Vector2(1,1), Vector2(0,2)]
        delau = Delaunay()
        tris = delau.triangulate(pts)
        # Should be at least 2 triangles (concave pentagon)
        assert len(tris) >= 2
        edges = delau.getEdges()
        assert len(edges) >= 6

class TestEdgeCasesAndErrors:
    def test_degenerate_all_points_colinear_or_less_than_3_points(self):
        delau = Delaunay()
        one_pt = [Vector2(1,1)]
        two_pts = [Vector2(0,0), Vector2(1,1)]
        # Should not crash -- expect no exception
        try:
            delau.triangulate(one_pt)
            delau.triangulate(two_pts)
        except Exception:
            pytest.fail("triangulate raised with degenerate input")