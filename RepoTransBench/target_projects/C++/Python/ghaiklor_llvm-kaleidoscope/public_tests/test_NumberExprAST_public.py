import pytest

class NumberExprAST:
    def __init__(self, val):
        self._val = val

def test_value_storage_public_test():
    testValue = 314.159
    numNode = NumberExprAST(testValue)
    # Since no public getters, just ensure instantiation works.
    assert hasattr(numNode, '_val')
    assert numNode._val == pytest.approx(314.159)