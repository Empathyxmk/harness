import ometa.vm_builder
import types

def test_PythonWriter_output_and_generateNode(monkeypatch):
    # Use a minimal valid node tree to activate more branches in ometa.vm_builder.PythonWriter
    class DummyTag:
        def __init__(self, name): self.name = name
    class Node:
        def __init__(self, tagname, data=None, args=None, span=None):
            self.tag = DummyTag(tagname)
            self.data = data
            self.args = args or []
            self.span = span
    class DummyOut:
        def __init__(self): self.lines = []; self.level = 0
        def writeln(self, l): self.lines.append(l)
        def indent(self): return self
    tree = Node('grammar', args=[
        Node('rule', args=[
            Node('name', data='arith'),
            Node('seq', args=[
                Node('anything'),
                Node('end')
            ])
        ])
    ])
    pyw = ometa.vm_builder.PythonWriter(tree, grammarText="FOO")
    out = DummyOut()
    pyw.output(out)
    assert out.lines

def test_GrammarEmitter_emit_rule(monkeypatch):
    # Patch PythonWriter so emitterForRule code path is used
    class DummyWriter:
        def __init__(self, expr): pass
        def output(self, o): o.emitted = True
    monkeypatch.setattr("ometa.vm_builder.PythonWriter", DummyWriter)
    emitter = ometa.vm_builder.GrammarEmitter("test")
    rule = {"tag": types.SimpleNamespace(name="rule"), "args": []}
    emitter.rules["R"] = rule
    res = emitter.emitterForRule("R")
    assert hasattr(res, "output") or hasattr(emitter, "emitted")

def test_opcode_emitter_emit(monkeypatch):
    # Cover OpcodeEmitter.emit() for multiple tags/branches
    emitter = ometa.vm_builder.OpcodeEmitter(None)
    assert emitter.emit(types.SimpleNamespace(tag=types.SimpleNamespace(name="null"), args=[])) is None
    assert emitter.emit(types.SimpleNamespace(tag=types.SimpleNamespace(name="end"), args=[])) is None
    assert emitter.emit(types.SimpleNamespace(tag=types.SimpleNamespace(name="anything"), args=[])) is None
    assert emitter.emit(types.SimpleNamespace(tag=types.SimpleNamespace(name="exactly"), args=["x"])) is None
    assert emitter.emit(types.SimpleNamespace(tag=types.SimpleNamespace(name="subrule"), args=["r", ["n"]])) is None