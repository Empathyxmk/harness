class DataFlowSolution:
    def __init__(self, in_map, out_map):
        self.in_map = dict(in_map)
        self.out_map = dict(out_map)

    def getValueBefore(self, key):
        return self.in_map.get(key, None)

    def getValueAfter(self, key):
        return self.out_map.get(key, None)

def test_different_in_out_values():
    in_map = {"A": 111, "B": 222}
    out_map = {"A": 777, "B": 888}
    dfs = DataFlowSolution(in_map, out_map)
    assert dfs.getValueBefore("A") == 111
    assert dfs.getValueBefore("B") == 222
    assert dfs.getValueAfter("A") == 777
    assert dfs.getValueAfter("B") == 888

def test_null_return_from_maps():
    in_map = {}
    out_map = {}
    dfs = DataFlowSolution(in_map, out_map)
    assert dfs.getValueBefore("notPresent") is None
    assert dfs.getValueAfter("notPresent") is None