import pytest

class NumberExprAST:
    def __init__(self, val):
        self._val = val

    def getValue(self):
        return self._val

    def codegen(self):
        # Returns a FakeLLVMValue unless the value is None
        return FakeLLVMValue(self._val)

class FakeLLVMValue:
    def __init__(self, value):
        self.value = value

def test_value_storage():
    numNode = NumberExprAST(42.5)
    assert numNode.getValue() == pytest.approx(42.5)

def test_codegen_returns_value():
    numNode = NumberExprAST(3.14)
    v = numNode.codegen()
    assert v is not None

def test_codegen_with_negative_value():
    numNode = NumberExprAST(-7.2)
    v = numNode.codegen()
    assert v is not None

def test_codegen_multiple_values():
    numNode1 = NumberExprAST(1.0)
    numNode2 = NumberExprAST(2.0)
    v1 = numNode1.codegen()
    v2 = numNode2.codegen()
    assert v1 is not None
    assert v2 is not None