import io
import ometa.builder
import pytest

def test_TextWriter_and_PythonWriter_integration():
    # Write a simple Python function using ometa.builder
    output = io.StringIO()
    tw = ometa.builder.TextWriter(output)
    tree = type('Node', (), {'tag': type('tag', (), {'name': 'null'}), 'args': [], 'span': None})
    pywriter = ometa.builder.PythonWriter(tree, grammarText="")
    pywriter.output(tw)
    result = output.getvalue()
    assert "None" in result or "return" in result

def test_generateNode_span(monkeypatch):
    # Test that code path with span in node is covered
    class DummyOut:
        def __init__(self): self.lines = []
        def writeln(self, l): self.lines.append(l)
        def indent(self): return self
    class DummyTag:
        def __init__(self, name): self.name = name
    class DummyNode:
        def __init__(self, tagname, span):
            self.tag = DummyTag(tagname)
            self.args = []
            self.span = span
    tree = DummyNode('null', span=(0, 2))
    pywriter = ometa.builder.PythonWriter(tree, grammarText="abc")
    pywriter._generateNode(DummyOut(), tree)