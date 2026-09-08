def test_different_constructor():
    class ProgramRepresentation:
        def getStartNode(self): return "alpha"
        def getExitNode(self): return "omega"
        def getPreds(self, n): return set()
        def getSuccs(self, n): return set()
        def getAllNodes(self): return {"alpha"}
        def getOwner(self, n): return "publicOwner"

    class OldForwardInterProceduralAnalysis:
        def __init__(self, pr, something):
            self.pr = pr
            self.something = something

        def apply(self, node, input_):
            return input_

    pr = ProgramRepresentation()
    ana = OldForwardInterProceduralAnalysis(pr, None)
    assert ana is not None