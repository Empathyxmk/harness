import pytest

# Simulate the necessary context for 'codegen'
class NumberExprAST:
    def __init__(self, val):
        self._val = val

    def codegen(self):
        # returns value as a FakeLLVMValue
        return FakeLLVMValue(self._val)

class FakeLLVMValue:
    def __init__(self, val):
        self.value = val

class ExprAST:
    def codegen(self):
        raise NotImplementedError

class BinaryExprAST:
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def codegen(self):
        # Simulates the codegen in C++.
        # Returns None if operation is not recognized or child is invalid.
        lhs_val = None if self.lhs is None else self.lhs.codegen()
        rhs_val = None if self.rhs is None else self.rhs.codegen()
        if lhs_val is None or rhs_val is None:
            return None
        if self.op == '+':
            return FakeLLVMValue(lhs_val.value + rhs_val.value)
        elif self.op == '-':
            return FakeLLVMValue(lhs_val.value - rhs_val.value)
        elif self.op == '*':
            return FakeLLVMValue(lhs_val.value * rhs_val.value)
        elif self.op == '<':
            # Fake as always return 1.0 for less-than comparisons
            return FakeLLVMValue(1.0 if lhs_val.value < rhs_val.value else 0.0)
        # Return None for unsupported op
        else:
            return None

def test_addition_codegen():
    lhs = NumberExprAST(3.0)
    rhs = NumberExprAST(5.0)
    node = BinaryExprAST('+', lhs, rhs)
    val = node.codegen()
    assert val is not None

def test_subtraction_codegen():
    lhs = NumberExprAST(8.0)
    rhs = NumberExprAST(2.0)
    node = BinaryExprAST('-', lhs, rhs)
    val = node.codegen()
    assert val is not None

def test_multiplication_codegen():
    lhs = NumberExprAST(2.0)
    rhs = NumberExprAST(4.0)
    node = BinaryExprAST('*', lhs, rhs)
    val = node.codegen()
    assert val is not None

def test_lessthan_codegen():
    lhs = NumberExprAST(1.0)
    rhs = NumberExprAST(2.0)
    node = BinaryExprAST('<', lhs, rhs)
    val = node.codegen()
    assert val is not None

def test_invalid_op_returns_none():
    lhs = NumberExprAST(1.0)
    rhs = NumberExprAST(2.0)
    node = BinaryExprAST('/', lhs, rhs)
    val = node.codegen()
    assert val is None

def test_codegen_returns_none_on_bad_children():
    class BadExprAST(ExprAST):
        def codegen(self):
            return None
    lhs = BadExprAST()
    rhs = NumberExprAST(1.0)
    node = BinaryExprAST('+', lhs, rhs)
    val = node.codegen()
    assert val is None