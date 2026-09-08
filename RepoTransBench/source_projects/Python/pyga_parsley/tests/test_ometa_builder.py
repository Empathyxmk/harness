import builtins
import types

import pytest

import ometa.builder

def test_TextWriter_writeln_and_indent(tmp_path):
    fileobj = tmp_path / "out.txt"
    with open(fileobj, "w") as f:
        writer = ometa.builder.TextWriter(f, indentSteps=2)
        writer.writeln("hello")
        writer.file.flush()
        inner = writer.indent()
        inner.writeln("hi")
    with open(fileobj, "r") as f:
        content = f.read()
    assert "hello" in content
    assert "hi" in content

class DummyTag:
    def __init__(self, name):
        self.name = name

class DummyNode:
    def __init__(self, tagname, args=(), span=None, data=None):
        self.tag = DummyTag(tagname)
        self.args = list(args)
        self.span = span
        self.data = data

def test_PythonWriter_gensym(monkeypatch):
    pw = ometa.builder.PythonWriter(tree=None, grammarText="")
    s1 = pw._gensym("foo")
    s2 = pw._gensym("foo")
    assert s1 != s2

def test_PythonWriter_expr(monkeypatch):
    pw = ometa.builder.PythonWriter(tree=None, grammarText="")
    class OUT:
        def __init__(self): self.lines = []
        def writeln(self, line): self.lines.append(line)
    name = pw._expr(OUT(), "test", "(3+5),None")
    assert name.startswith("_G_test_")

def test_PythonWriter_writeFunction(monkeypatch):
    pw = ometa.builder.PythonWriter(tree=None, grammarText="")
    class OUT:
        def __init__(self): self.lines = []
        def writeln(self, line): self.lines.append(line)
        def indent(self): return self
    out = OUT()
    pw._writeFunction(out, "fname", ("a",), DummyNode("null"))
    assert any("def fname" in l for l in out.lines)

def test_PythonWriter_compilePythonExpr(monkeypatch):
    pw = ometa.builder.PythonWriter(tree=None, grammarText="")
    class OUT:
        def __init__(self): self.lines = []
        def writeln(self, line): self.lines.append(line)
    a = pw.compilePythonExpr(OUT(), "12345")
    b = pw.compilePythonExpr(OUT(), "x+y")
    # compiledExprCache case
    pw.compiledExprCache = {}
    c = pw.compilePythonExpr(OUT(), "x+y")
    assert a and b and c

def test_PythonWriter__generate(monkeypatch):
    outcalls = []
    class OUT:
        def writeln(self, l): outcalls.append(l)
        def indent(self): return self
    node = DummyNode("null")
    pw = ometa.builder.PythonWriter(tree=node, grammarText="")
    pw._generate(OUT(), node, retrn=True)
    assert any("return (" in s for s in outcalls)