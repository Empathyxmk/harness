class DataFlowSolution:
    def __init__(self):
        self.map = {}
    def set(self, k, v):
        self.map[k] = set(v)
    def get(self, k):
        return self.map.get(k, set())
    def keySet(self):
        return set(self.map.keys())
    def merge(self, other):
        for k, v in other.map.items():
            if k in self.map:
                self.map[k] = self.map[k].union(v)
            else:
                self.map[k] = set(v)
    def __str__(self):
        return f"DataFlowSolution({self.map})"

def test_set_and_get():
    dfs = DataFlowSolution()
    dfs.set("A", [42])
    assert 42 in dfs.get("A")
    assert "A" in dfs.keySet()

def test_merge():
    dfs1 = DataFlowSolution()
    dfs2 = DataFlowSolution()
    dfs1.set("A", [1])
    dfs2.set("A", [2])
    dfs1.merge(dfs2)
    got = dfs1.get("A")
    assert 1 in got
    assert 2 in got

def test_to_string():
    dfs = DataFlowSolution()
    dfs.set("B", [100])
    s = str(dfs)
    assert "B" in s