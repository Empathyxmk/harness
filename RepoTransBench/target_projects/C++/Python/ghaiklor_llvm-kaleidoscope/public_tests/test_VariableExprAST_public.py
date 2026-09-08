class VariableExprAST:
    def __init__(self, name):
        self._name = name

def test_construction_public_test():
    var = VariableExprAST("beta")
    # Just ensure no exceptions and the instance is created.
    assert isinstance(var, VariableExprAST)
    assert var._name == "beta"