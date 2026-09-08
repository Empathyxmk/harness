def test_basic_constructor():
    class ProgramRepresentation:
        def getStartNode(self): return "start"
        def getExitNode(self): return "exit"
        def getPreds(self, n): return set()
        def getSuccs(self, n): return set()
        def getAllNodes(self): return {"start"}
        def getOwner(self, n): return "owner"

    class OldForwardInterProceduralAnalysis:
        def __init__(self, pr, something):
            self.pr = pr
            self.something = something

        def apply(self, node, input_):
            return input_

    pr = ProgramRepresentation()
    ana = OldForwardInterProceduralAnalysis(pr, None)
    assert ana is not None