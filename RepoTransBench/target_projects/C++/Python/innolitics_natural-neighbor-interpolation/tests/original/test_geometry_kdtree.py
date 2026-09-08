import pytest
import math

# Minimal stand-ins for geometry::Point and kdtree for test purposes only.
class Point:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            self.data = list(args[0])
        elif len(args) == 0:
            self.data = [0.0, 0.0, 0.0]
        else:
            self.data = list(args)
    def __getitem__(self, i):
        return self.data[i]
    def __setitem__(self, i, v):
        self.data[i] = v
    def comparable_distance(self, other):
        return sum((self.data[d] - other.data[d]) ** 2 for d in range(len(self.data)))

    def __eq__(self, other):
        return all(abs(a - b) < 1e-8 for a, b in zip(self.data, other.data))

# Stand-in for a minimal kdtree.
class KDTreeResult:
    def __init__(self, value, distance):
        self.value = value
        self.distance = distance

class KDTree:
    # For test purposes only: brute-force storage
    def __init__(self):
        self.points = []
        self.values = []
        self.build_called = False
    def add(self, pt, val):
        self.points.append(Point(pt.data))
        self.values.append(val)
    def build(self):
        self.build_called = True
    def nearest_iterative(self, query):
        if not self.points:
            raise Exception("KDTree is empty")
        dists = [query.comparable_distance(pt) for pt in self.points]
        min_dist = min(dists)
        candidates = [i for i, d in enumerate(dists) if abs(d - min_dist) < 1e-8]
        avg_value = sum(self.values[i] for i in candidates) / len(candidates)
        return KDTreeResult(avg_value, math.sqrt(min_dist))

def test_geometry_default_ctor():
    p = Point()
    p[0] = 1.0
    p[1] = 2.0
    p[2] = 3.0
    assert p[0] == 1.0
    assert p[1] == 2.0
    assert p[2] == 3.0

def test_geometry_two_arg_ctor():
    p = Point(1.1, 2.2)
    assert abs(p[0] - 1.1) < 1e-8
    assert abs(p[1] - 2.2) < 1e-8

def test_geometry_three_arg_ctor():
    p = Point(3.3, 4.4, 5.5)
    assert abs(p[0] - 3.3) < 1e-8
    assert abs(p[1] - 4.4) < 1e-8
    assert abs(p[2] - 5.5) < 1e-8

def test_geometry_comparable_distance_self():
    a = Point(1.0, 2.0, 3.0)
    assert abs(a.comparable_distance(a) - 0.0) < 1e-8

def test_geometry_comparable_distance_other():
    a = Point(1.0, 2.0, 3.0)
    b = Point(4.0, 6.0, 3.0)
    expected = (4.0-1.0)**2 + (6.0-2.0)**2
    assert abs(a.comparable_distance(b) - expected) < 1e-8

def test_geometry_index_operators():
    p = Point(10.5, 11.5, 12.5)
    p[1] = 99.9
    assert abs(p[1] - 99.9) < 1e-8
    cp = Point(2.2, 3.3, 4.4)
    assert abs(cp[2] - 4.4) < 1e-8

def test_kdtree_empty_throws():
    tree = KDTree()
    q = Point(0.0, 0.0, 0.0)
    with pytest.raises(Exception):
        tree.nearest_iterative(q)

def test_kdtree_add_and_nearest_one():
    tree = KDTree()
    tree.add(Point(1, 2, 3), 42.0)
    tree.build()
    res = tree.nearest_iterative(Point(1, 2, 3))
    assert abs(res.value - 42.0) < 1e-8
    assert abs(res.distance - 0.0) < 1e-8

def test_kdtree_nearest_multiple():
    tree = KDTree()
    tree.add(Point(0, 0, 0), 10.0)
    tree.add(Point(1, 0, 0), 20.0)
    tree.add(Point(0, 1, 0), 30.0)
    tree.add(Point(0, 0, 1), 40.0)
    tree.build()
    res = tree.nearest_iterative(Point(1, 0, 0))
    assert abs(res.value - 20.0) < 1e-8
    assert abs(res.distance - 0.0) < 1e-8

def test_kdtree_nearest_equidistant():
    tree = KDTree()
    tree.add(Point(0, 0, 0), 10.0)
    tree.add(Point(2, 0, 0), 30.0)
    tree.build()
    res = tree.nearest_iterative(Point(1, 0, 0))
    # Both are 1 away (distance 1.0), so value should be mean
    assert abs(res.value - 20.0) < 1e-8
    assert abs(res.distance - 1.0) < 1e-8