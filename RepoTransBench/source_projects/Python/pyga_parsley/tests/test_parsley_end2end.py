import parsley
import pytest

class DummyParseError(Exception):
    pass

def test_end2end_sanity(monkeypatch):
    # Fully simulate an end-to-end roundtrip using a stub OMeta API.
    class DummyOMeta:
        @staticmethod
        def makeGrammar(source, name):
            class DummyGram:
                def createParserClass(self, base, bindings):
                    class ParserStub:
                        def __init__(self, inp):
                            self.input = inp
                            self._trace = None
                        def apply(self, rule, *args):
                            if rule == "foo":
                                return ("PASS", None)
                            raise parsley.ParseError("fail", 1, [], None)
                    return ParserStub
            return DummyGram()
    monkeypatch.setattr(parsley, "OMeta", DummyOMeta)
    make = parsley.makeGrammar("grammar", {}, unwrap=False)
    parser = make("abc")
    assert parser.foo() == "PASS"
    with pytest.raises(Exception):
        parser.bar()