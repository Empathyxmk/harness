def test_basic_usage():
    class PointsToGraph:
        def __init__(self):
            self.data = {}
        def add(self, a, b):
            self.data.setdefault(a, set()).add(b)
        def get(self, a):
            return self.data.get(a, set())
        def merge(self, that):
            for k, vs in that.data.items():
                self.data.setdefault(k, set()).update(vs)

    ptg = PointsToGraph()
    ptg.add("a", "x")
    ptg.add("a", "y")
    ptg.add("b", "z")
    assert "x" in ptg.get("a")
    assert "y" in ptg.get("a")
    assert "z" in ptg.get("b")
    assert "z" not in ptg.get("a")

def test_merge():
    class PointsToGraph:
        def __init__(self):
            self.data = {}
        def add(self, a, b):
            self.data.setdefault(a, set()).add(b)
        def get(self, a):
            return self.data.get(a, set())
        def merge(self, that):
            for k, vs in that.data.items():
                self.data.setdefault(k, set()).update(vs)

    g1 = PointsToGraph()
    g2 = PointsToGraph()
    g1.add("A", "one")
    g2.add("A", "two")
    g1.merge(g2)
    g1s = g1.get("A")
    assert "one" in g1s
    assert "two" in g1s