class ExprAST:
    pass

class NumberExprAST(ExprAST):
    def __init__(self, value):
        self.value = value

class CallExprAST(ExprAST):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

def test_construction_with_args_public_test():
    args = [NumberExprAST(202.024)]
    call = CallExprAST("anotherPublicFunc", args)
    assert call.callee == "anotherPublicFunc"
    assert isinstance(call.args[0], NumberExprAST)
    assert call.args[0].value == 202.024