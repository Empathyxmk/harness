import pytest
import ometa.vm_builder

class DummyTerm:
    def __init__(self, tag, data=None, args=[]):
        self.tag = type('tag', (), {'name': tag})
        self.data = data
        self.args = list(args)

def test_writeBytecode(monkeypatch):
    monkeypatch.setattr('builtins.open', lambda fn, *a, **k: type('FakeFile', (), {'read': staticmethod(lambda: 'grammar')})())
    class DummyGrammar:
        @staticmethod
        def makeGrammar(text, name):
            class DummyG:
                def createParserClass(self, base, bindings):
                    class DummyParser:
                        def transform(self, expr): return ["OUT1"]
                    return DummyParser
            return DummyG()
    monkeypatch.setattr("ometa.grammar.TreeTransformerGrammar", DummyGrammar)
    monkeypatch.setattr("ometa.runtime.TreeTransformerBase", object)
    ret = ometa.vm_builder.writeBytecode("EXPR")
    assert ret == "OUT1"

def test_bytecodeToPython(monkeypatch):
    monkeypatch.setattr('builtins.open', lambda fn, *a, **k: type('FakeFile', (), {'read': staticmethod(lambda: 'grammar')})())
    class DummyGrammar:
        @staticmethod
        def makeGrammar(text, name):
            class DummyG:
                def createParserClass(self, base, bindings):
                    class DummyParser:
                        def transform(self, expr): return ["emitted"]
                    return DummyParser
            return DummyG()
    monkeypatch.setattr("ometa.grammar.TreeTransformerGrammar", DummyGrammar)
    monkeypatch.setattr("ometa.runtime.TreeTransformerBase", object)
    ret = ometa.vm_builder.bytecodeToPython("EXPR")
    assert ret == "emitted"

def test_writeBytecodeRule_and_Grammar(monkeypatch):
    class DummyPW:
        def __init__(self, expr): self.expr = expr
        def output(self, out): out.rules["a"] = "b"
    monkeypatch.setattr("ometa.vm_builder.PythonWriter", DummyPW)
    class DummyEmitter:
        def __init__(self): self.rules = {}; self.tree = False
        def emitterForRule(self, name): self.rules[name] = []; return self
    monkeypatch.setattr("ometa.vm_builder.GrammarEmitter", DummyEmitter)
    expr = "x"
    res = ometa.vm_builder.writeBytecodeRule(expr)
    assert isinstance(res, tuple)
    out = ometa.vm_builder.writeBytecodeGrammar(expr)
    assert isinstance(out, dict)