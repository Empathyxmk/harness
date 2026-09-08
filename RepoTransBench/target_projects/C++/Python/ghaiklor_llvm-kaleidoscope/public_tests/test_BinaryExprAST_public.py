class NumberExprAST:
    def __init__(self, value):
        self.value = value

class BinaryExprAST:
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

def test_construction_public_test():
    left = NumberExprAST(10.31)
    right = NumberExprAST(-5.62)
    expr = BinaryExprAST('%', left, right)
    assert expr.op == '%'
    assert expr.lhs.value == 10.31
    assert expr.rhs.value == -5.62