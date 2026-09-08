def test_basic_coverage():
    class CallGraph:
        def __init__(self):
            self.edges = {}
        def addEdge(self, a, b):
            self.edges.setdefault(a, set()).add(b)
        def getCallees(self, a):
            return self.edges.get(a, set())
        def getCallers(self, b):
            return {src for src, tgts in self.edges.items() if b in tgts}

    cg = CallGraph()
    cg.addEdge("A", "B")
    cg.addEdge("A", "C")
    cg.addEdge("B", "D")
    assert "B" in cg.getCallees("A")
    assert "C" in cg.getCallees("A")
    assert len(cg.getCallees("A")) == 2
    assert "A" in cg.getCallers("B")
    assert "B" not in cg.getCallees("C")