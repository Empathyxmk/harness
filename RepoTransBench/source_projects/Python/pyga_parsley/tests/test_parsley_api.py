import pytest
import types

import parsley

def test_wrapGrammar_and_unwrapGrammar():
    class Dummy:
        def __init__(self, x):
            self.val = x
    make = parsley.wrapGrammar(Dummy)
    parser = make("abc")
    assert isinstance(parser, parsley._GrammarWrapper)
    assert parser._input == "abc"
    assert parsley.unwrapGrammar(make) == Dummy
    # unwrapGrammar: should return same for bare class
    assert parsley.unwrapGrammar(Dummy) == Dummy

def test__GrammarWrapper_getattr_success_and_eof(monkeypatch):
    # Rule returns a value and EOF is raised -> should return value
    class DummyInput:
        def head(self):
            raise parsley.EOFError()

    class DummyGrammar:
        def __init__(self):
            self.input = DummyInput()
        def apply(self, name, *args):
            return ("foo", "info")
    wrapper = parsley._GrammarWrapper(DummyGrammar(), "abc")
    assert wrapper.bar() == "foo"

def test__GrammarWrapper_getattr_ParseError(monkeypatch):
    class DummyParseError(Exception): pass
    class DummyG:
        def apply(self, name, *args):
            raise parsley.ParseError("input", 2, [["msg", "err"]], None)
        def considerError(self, err):
            self.currentError = err
        currentError = None
        input = None
    wrapper = parsley._GrammarWrapper(DummyG(), "in")
    with pytest.raises(Exception):
        wrapper.anything()

def test__GrammarWrapper_getattr_input_remains(monkeypatch):
    # When input remains, apply returns a value, but head() does not raise
    class DummyErr(Exception): pass
    class DummyInput:
        def head(self):
            return "more", None
    class DummyG:
        def __init__(self):
            self.input = DummyInput()
        def apply(self, name, *args):
            return ("foo", DummyErr("err"))
        def considerError(self, err):
            self.currentError = err
        currentError = DummyErr("err")
    wrapper = parsley._GrammarWrapper(DummyG(), "abc")
    with pytest.raises(DummyErr):
        wrapper.anything()
        
def test_makeGrammar_unwrap(monkeypatch):
    # monkeypatch OMeta.makeGrammar and .createParserClass
    called = {}
    def fake_createParserClass(base, binds):
        called['called'] = True
        class Dummy: pass
        return Dummy
    class DummyOMeta:
        def makeGrammar(self, src, name):
            class DummyClass:
                def createParserClass(self, base, binds):
                    return fake_createParserClass(base, binds)
            return DummyClass()
    monkeypatch.setattr(parsley, "OMeta", DummyOMeta())
    g = parsley.makeGrammar("a = b", {"x": 1}, unwrap=True)
    assert called['called']

def test_makeGrammar_no_unwrap(monkeypatch):
    class DummyWrapper:
        pass
    class DummyClass:
        pass
    def fake_wrapGrammar(g, tracefunc=None): return DummyWrapper
    def fake_createParserClass(base, binds): return DummyClass
    class DummyOMeta:
        def makeGrammar(self, src, name):
            class Dummy:
                def createParserClass(self, base, binds):
                    return DummyClass
            return Dummy()
    monkeypatch.setattr(parsley, "OMeta", DummyOMeta())
    monkeypatch.setattr(parsley, "wrapGrammar", fake_wrapGrammar)
    res = parsley.makeGrammar("src", {}, unwrap=False)
    assert res is DummyWrapper

def test_makeProtocol(monkeypatch):
    class DummyGrammar:
        def parseGrammar(self, name): return "grammar"
    class DummyOMeta:
        def __init__(self, src): pass
        def parseGrammar(self, name): return "grammar"
    class DummyProtocol:
        def __init__(self, grammar, senderFactory, receiverFactory, bindings):
            self.args = (grammar, senderFactory, receiverFactory, bindings)
    monkeypatch.setattr(parsley, "OMeta", DummyOMeta)
    import functools as ft
    monkeypatch.setattr("ometa.protocol.ParserProtocol", DummyProtocol)
    source = "S"
    S, R = lambda x: x, lambda x: x
    fac = parsley.makeProtocol(source, S, R, bindings={'a': 1}, name='TestGrammar')
    pp = fac()
    assert pp.args[0] == "grammar"
    assert callable(fac)

def test_stack_basic():
    def one(x): return "A" + str(x)
    def two(x): return "B" + str(x)
    f = parsley.stack(one, two)
    assert callable(f)
    assert f("z") == "A" + "B" + "z"

def test_stack_empty():
    f = parsley.stack()
    with pytest.raises(TypeError):
        f('a')