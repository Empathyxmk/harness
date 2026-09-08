class PrototypeAST:
    def __init__(self, name, args):
        self._name = name
        self._args = args

    def getName(self):
        return self._name

def test_construction_and_getter_public_test():
    args = ["zeta", "theta"]
    proto = PrototypeAST("cosmopub", args)
    assert proto.getName() == "cosmopub"