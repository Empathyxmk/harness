import pytest

# Simulate the NamedValues dict that is used in codegen lookup.
NamedValues = {}

class VariableExprAST:
    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    def codegen(self):
        # Returns None if variable is not in NamedValues or the value is None,
        # simulating behavior from C++ code.
        if self._name not in NamedValues:
            return None
        if NamedValues[self._name] is None:
            return None
        return NamedValues[self._name]

def test_get_variable_name():
    var = VariableExprAST("x")
    assert var.getName() == "x"

def test_codegen_unknown_variable():
    var = VariableExprAST("y")
    # Variable not in NamedValues, expect None
    assert var.codegen() is None

def test_codegen_after_setting_variable():
    var = VariableExprAST("z")
    # Add to NamedValues (simulate LLVM AllocaInst as None)
    NamedValues["z"] = None
    assert var.codegen() is None
    NamedValues.pop("z", None)