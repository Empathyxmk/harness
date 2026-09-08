def test_program_representation_different_nodes():
    class ProgramRepresentation:
        def getStartNode(self): return "publicStart"
        def getExitNode(self): return "publicExit"
        def getPreds(self, n): return ["predX"]
        def getSuccs(self, n): return ["succY"]
        def getAllNodes(self): return ["publicStart", "publicExit"]
        def getOwner(self, n): return "ownerZ"

    pr = ProgramRepresentation()
    assert pr.getStartNode() == "publicStart"
    assert pr.getExitNode() == "publicExit"
    assert pr.getOwner("publicStart") == "ownerZ"
    assert len(list(pr.getPreds("publicExit"))) > 0
    assert len(list(pr.getSuccs("publicStart"))) > 0

def test_null_iterables():
    class ProgramRepresentation:
        def getStartNode(self): return "begin"
        def getExitNode(self): return "finish"
        def getPreds(self, n): return None
        def getSuccs(self, n): return None
        def getAllNodes(self): return None
        def getOwner(self, n): return None

    pr = ProgramRepresentation()
    assert pr.getStartNode() == "begin"
    assert pr.getExitNode() == "finish"
    assert pr.getOwner("whatever") is None