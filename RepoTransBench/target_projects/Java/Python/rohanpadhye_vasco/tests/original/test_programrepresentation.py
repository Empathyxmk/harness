def test_basic_override():
    class ProgramRepresentation:
        def getStartNode(self): return "start"
        def getExitNode(self): return "exit"
        def getPreds(self, n): return None
        def getSuccs(self, n): return None
        def getAllNodes(self): return None
        def getOwner(self, n): return None

    pr = ProgramRepresentation()
    assert pr.getStartNode() == "start"
    assert pr.getExitNode() == "exit"
    assert pr.getPreds("x") is None