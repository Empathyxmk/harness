def test_coverage():
    class CallGraph:
        def __init__(self):
            self.edges = {}
        def addEdge(self, a, b):
            self.edges.setdefault(a, set()).add(b)
        def getCallees(self, a):
            return self.edges.get(a, set())
    class CallGraphTransformer:
        def transform(self, graph):
            graph.addEdge("B", "C")

    cg = CallGraph()
    cg.addEdge("A", "B")
    t = CallGraphTransformer()
    t.transform(cg)
    assert "C" in cg.getCallees("B")