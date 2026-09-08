import math
import pytest
from dt.vector2 import Vector2
from dt.edge import Edge
from dt.triangle import Triangle
from dt.delaunay import Delaunay

class TestVector2PublicOperations:
    def test_constructor_and_access(self):
        v1 = Vector2(2.0, 3.0)
        v2 = Vector2(5.0, 9.0)
        assert v1.x == 2.0
        assert v2.y == 9.0

    def test_equality_operator(self):
        v1 = Vector2(2.0, 3.0)
        v2 = Vector2(5.0, 9.0)
        v3 = Vector2(2.0, 3.0)
        assert v1 == v3
        assert not (v1 == v2)

    def test_dist2_and_norm2(self):
        v1 = Vector2(2.0, 3.0)
        v2 = Vector2(5.0, 9.0)
        assert pytest.approx(v1.dist2(v2), rel=1e-8) == 45.0
        assert pytest.approx(v1.norm2(), rel=1e-8) == 13.0

    def test_dist_specialized(self):
        v2 = Vector2(5.0, 9.0)
        v3 = Vector2(0.0, 0.0)
        assert pytest.approx(v2.dist(v3), rel=1e-8) == math.sqrt(106.0)

    def test_ostream_operator(self):
        v2 = Vector2(5.0, 9.0)
        s = str(v2)
        assert "Point x: 5" in s

class TestEdgePublicFunctionality:
    def test_construction_and_equality(self):
        v1 = Vector2(3.0, 2.0)
        v2 = Vector2(6.0, 4.0)
        e1 = Edge(v1, v2)
        e2 = Edge(v2, v1)
        e3 = Edge(v1, v1)
        assert e1 == e2
        assert not (e1 == e3)

    def test_ostream_operator(self):
        v1 = Vector2(3.0, 2.0)
        v2 = Vector2(6.0, 4.0)
        e2 = Edge(v2, v1)
        s = str(e2)
        assert "Edge" in s

class TestTrianglePublicLogic:
    def test_contains_vertex(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(5.0, 1.0)
        v3 = Vector2(1.0, 4.0)
        tri = Triangle(v1, v2, v3)
        assert tri.containsVertex(v3)
        assert not tri.containsVertex(Vector2(2.0, 2.0))

    def test_circumcircle_contains(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(5.0, 1.0)
        v3 = Vector2(1.0, 4.0)
        tri = Triangle(v1, v2, v3)
        inside = Vector2(2, 2)
        outside = Vector2(7, 7)
        assert tri.circumCircleContains(inside)
        assert not tri.circumCircleContains(outside)

    def test_operator_eq_for_triangles(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(5.0, 1.0)
        v3 = Vector2(1.0, 4.0)
        tri = Triangle(v1, v2, v3)
        tri2 = Triangle(v1, v2, v3)
        tri3 = Triangle(v3, v2, v1)
        v4 = Vector2(7.0, 7.0)
        tri4 = Triangle(v1, v2, v4)
        assert tri == tri2
        assert tri == tri3
        assert not (tri == tri4)

    def test_ostream_operator(self):
        v1 = Vector2(1.0, 1.0)
        v2 = Vector2(5.0, 1.0)
        v3 = Vector2(1.0, 4.0)
        tri = Triangle(v1, v2, v3)
        s = str(tri)
        assert "Triangle" in s

class TestDelaunayPublicAlgorithm:
    def test_basic_triangulation_works_for_public_minimal_points(self):
        points = [Vector2(10.0, 10.0), Vector2(14.0, 10.0), Vector2(10.0, 13.0)]
        delaunay = Delaunay()
        triangles = delaunay.triangulate(points)
        assert len(triangles) == 1
        verts = delaunay.getVertices()
        assert len(verts) == 3

    def test_edges_are_present(self):
        points = [Vector2(10.0, 10.0), Vector2(14.0, 10.0), Vector2(10.0, 13.0)]
        delaunay = Delaunay()
        delaunay.triangulate(points)
        edges = delaunay.getEdges()
        assert len(edges) == 3

    def test_get_triangles_reference(self):
        points = [Vector2(10.0, 10.0), Vector2(14.0, 10.0), Vector2(10.0, 13.0)]
        delaunay = Delaunay()
        delaunay.triangulate(points)
        tris = delaunay.getTriangles()
        assert len(tris) == 1

class TestDelaunayLargerPublicInput:
    def test_larger_public_input(self):
        pts = [Vector2(10,10), Vector2(11,10), Vector2(12,10), Vector2(11,11), Vector2(10,12)]
        delau = Delaunay()
        tris = delau.triangulate(pts)
        # Should be at least 2 triangles (concave pentagon)
        assert len(tris) >= 2
        edges = delau.getEdges()
        assert len(edges) >= 6

class TestPublicEdgeCasesAndErrors:
    def test_degenerate_all_points_colinear_or_less_than_3_points_public(self):
        delau = Delaunay()
        one_pt = [Vector2(10,10)]
        two_pts = [Vector2(10,10), Vector2(20,20)]
        try:
            delau.triangulate(one_pt)
            delau.triangulate(two_pts)
        except Exception:
            pytest.fail("triangulate raised with degenerate input")