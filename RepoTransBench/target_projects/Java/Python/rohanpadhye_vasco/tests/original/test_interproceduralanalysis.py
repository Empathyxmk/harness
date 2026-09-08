def test_trivial_analysis():
    class ProgramRepresentation:
        def getStartNode(self): return "start"
        def getExitNode(self): return "exit"
        def getPreds(self, n): return None
        def getSuccs(self, n): return None
        def getAllNodes(self): return None
        def getOwner(self, n): return None

    class ForwardInterProceduralAnalysis:
        def __init__(self, pr, something):
            self.pr = pr
            self.something = something
        def apply(self, node, input_):
            return input_

    pr = ProgramRepresentation()
    analysis = ForwardInterProceduralAnalysis(pr, None)
    assert analysis is not None