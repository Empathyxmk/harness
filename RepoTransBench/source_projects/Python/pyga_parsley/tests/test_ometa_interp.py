import pytest
import types

import ometa.interp


def dummy_callback(*a, **kw):
    dummy_callback.calls.append((a, kw))
dummy_callback.calls = []


class DummyInput:
    def __init__(self):
        self.data = []
        self._memo = {}
        self.position = 0
    def getMemo(self, ruleName): return self._memo.get(ruleName)
    def setMemo(self, ruleName, val): self._memo[ruleName] = val; return val
    def nullError(self): return ValueError("nullError")
    def extend(self, data): self.data.extend(data)
    def __eq__(self, other): return True

def test_decomposeGrammar_basic():
    class Tag:
        def __init__(self, name): self.name = name
    class Node:
        def __init__(self, tag, args=[]): self.tag = tag; self.args = args
    tag_rule = Tag('Rule')
    grammar = Node(Tag('Grammar'), [None, None, Node(None, [Node(tag_rule, [type('Obj', (), {'data':'r1'})(), 'expr1'])])])
    rules = ometa.interp.decomposeGrammar(grammar)
    assert 'r1' in rules

def test_TrampolinedGrammarInterpreter_receive_and_end(monkeypatch):
    class DummyGrammar:
        tag = type('tag', (), {'name': 'Grammar'})()
        def __init__(self): self.args = [None,None, type('x', (), {'args':[]})()]
    ti = ometa.interp.TrampolinedGrammarInterpreter(DummyGrammar(), "foo", callback=dummy_callback)
    ti.input = DummyInput()
    # End with no input
    ti.ended = False
    ti.position = 0
    ti.receive([])
    ti.ended = True
    with pytest.raises(ValueError):
        ti.receive(['x'])
    # Feed
    ti.ended = False
    calls = []
    def next_gen():
        yield None
        yield (1,2)
    ti.next = next_gen()
    ti.input = DummyInput()
    ti.input.data = []
    ti.receive(['a'])
    # end
    ti.ended = False
    ti.next = next_gen()
    ti.end()
    ti.ended = True
    ti.end()

def test_TrampolinedGrammarInterpreter_setNext_and__apply(monkeypatch):
    class DummyGrammar:
        tag = type('tag', (), {'name': 'Grammar'})()
        def __init__(self): self.args = [None,None, type('x', (), {'args':[]})()]
    g = ometa.interp.TrampolinedGrammarInterpreter(DummyGrammar(), "foo")
    def fun(): yield "val"
    it = g._apply(fun, "rule", ())
    assert list(it)[0] == "val"
    g.input = DummyInput()
    g.input._memo.clear()
    # LeftRecursion
    class LR:
        detected = False
    g.input._memo["rule2"] = LR()
    def fun2(): return iter(())
    with pytest.raises(ValueError):
        list(g._apply(fun2, "rule2", ()))

def test_TrampolinedGrammarInterpreter__eval(monkeypatch):
    class DummyRule:
        tag = type("tag", (), {"name": "Apply"})
        args = [type("x", (), {"data": "r"}), type("x", (), {"data": "c"}), type("x", (), {"args": []})]
    ti = ometa.interp.TrampolinedGrammarInterpreter(type('G', (), {'tag': type('tag',(),{'name':'Grammar'})(), 'args':[None,None,type('x', (), {'args':[]})()]})(), "foo")
    ti.input = DummyInput()
    def apply(*a, **k):
        yield "passed"
    ti.apply = apply
    list(ti._eval(DummyRule()))