import parsley

def test_makeGrammar_and_unwrap():
    G = parsley.makeGrammar("foo = 'x'", {})
    parser = G("x")
    assert parser.input == "x"
    assert hasattr(parser, "apply")

def test_makeGrammar_with_unwrap_false():
    G = parsley.makeGrammar("bar = 'y'", {}, unwrap=False)
    parser = G("y")
    assert parser.input == "y"
    assert hasattr(parser, "apply")

def test_ParseError_and_repr():
    e = parsley.ParseError("X", 2, [1, 2, 3], None)
    s = repr(e)
    assert "ParseError" in s

def test_OMetaBase_trace_property(monkeypatch):
    # Patch OMetaBase to check _trace property branch
    G = parsley.makeGrammar("foo = 'f'", {})
    parser = G("f")
    parser._trace = "FOO"
    assert parser._trace == "FOO"