import pytest

# Simulate global LLVM "module" for context stub
TheModule = None
TheContext = None

class PrototypeAST:
    def __init__(self, name, args):
        self._name = name
        self._args = args

    def codegen(self):
        # In real implementation, would produce an LLVM function.
        # Simulate: return a 'FakeFunction' with the right arg size and name.
        return FakeFunction(self._name, self._args)

class FakeFunction:
    def __init__(self, name, args):
        self._name = name
        self._args = args

    def arg_size(self):
        return len(self._args)

    def getName(self):
        return self._name

def test_codegen_creates_function():
    global TheModule
    TheModule = object()  # stub as in C++, TheModule assigned
    args = ["x", "y"]
    proto = PrototypeAST("foo", args)
    fn = proto.codegen()
    assert fn is not None
    assert fn.arg_size() == 2
    assert fn.getName() == "foo"