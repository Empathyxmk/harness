import pytest
import ometa.grammar

def test_grammar_makeGrammar(monkeypatch):
    # Patch OMetaGrammar's createParserClass
    class DummyGram:
        def createParserClass(self, base, bindings):
            class Parser:
                def __init__(self, inp): self.input = inp
                def apply(self, rule): return True
            return Parser
    monkeypatch.setattr(ometa.grammar, "ParserBase", object)
    g = ometa.grammar.OMetaGrammar("grammar", {})
    g.grammar = DummyGram()
    parser = g("abc")
    assert parser.input == "abc"

def test_OMetaGrammar___call__exception(monkeypatch):
    # __call__ with no grammar should raise
    g = ometa.grammar.OMetaGrammar("source", {})
    g.grammar = None
    with pytest.raises(Exception):
        g("a")

def test_OMetaGrammar_repr():
    g = ometa.grammar.OMetaGrammar("foo = 'a'", {})
    s = repr(g)
    assert "OMetaGrammar" in s