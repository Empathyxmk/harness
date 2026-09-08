import pytest

class ExprAST:
    def codegen(self):
        raise NotImplementedError

class NumberExprAST(ExprAST):
    def __init__(self, val):
        self._val = val

    def codegen(self):
        return FakeLLVMValue(self._val)

class FakeLLVMValue:
    def __init__(self, val):
        self.value = val

# "Function" registry to simulate symbol table for functions
RegisteredFunctions = {}

class CallExprAST(ExprAST):
    def __init__(self, callee, args):
        self._callee = callee
        self._args = args

    def getCallee(self):
        return self._callee

    def codegen(self):
        # Simulates codegen logic
        # If callee not in RegisteredFunctions, return None
        # If any arg is None, return None
        if self._callee not in RegisteredFunctions:
            return None
        for arg in self._args:
            if arg is None:
                return None
            if arg.codegen() is None:
                return None
        return FakeLLVMValue(123.456)  # value is not checked in these tests

def test_get_function_name():
    call = CallExprAST("myfunc", [])
    assert call.getCallee() == "myfunc"

def test_call_with_no_args():
    call = CallExprAST("test_noargs", [])
    assert call.codegen() is None

def test_call_with_args_returns_none_if_args_are_none():
    args = [None]
    call = CallExprAST("test_nullargs", args)
    assert call.codegen() is None

def test_codegen_unknown_function():
    call = CallExprAST("nonexistent", [])
    assert call.codegen() is None

def test_call_with_number_argument():
    args = [NumberExprAST(55)]
    call = CallExprAST("fakefunc", args)
    assert call.codegen() is None