import pytest
from pythonflow.core import Graph, Operation

class DummyOp(Operation):
    # minimal operation for testing graph
    def _evaluate(self):
        return 42

def test_graph_enter_exit():
    g = Graph()
    assert getattr(g._globals, 'default_graph', None) is None
    with g:
        assert Graph._globals.default_graph is g
    assert getattr(g._globals, 'default_graph', None) is None

def test_graph_duplicate_enter():
    g = Graph()
    with g:
        with pytest.raises(AssertionError):
            with g:
                pass

def test_graph_normalize_operation_with_instance():
    g = Graph()
    op = DummyOp(name="abc", graph=g)
    g.operations["abc"] = op
    assert g.normalize_operation(op) is op
    # Bad graph
    other = Graph()
    op2 = DummyOp(name="def", graph=other)
    with pytest.raises(RuntimeError):
        g.normalize_operation(op2)

def test_graph_normalize_operation_with_name():
    g = Graph()
    op = DummyOp(name="abc", graph=g)
    g.operations["abc"] = op
    assert g.normalize_operation("abc") is op

def test_graph_normalize_operation_invalid():
    g = Graph()
    with pytest.raises(ValueError):
        g.normalize_operation(123)
    with pytest.raises(KeyError):
        g.normalize_operation("notfound")

def test_graph_normalize_context_and_duplicates():
    g = Graph()
    op = DummyOp(name='x', graph=g)
    g.operations['x'] = op
    # context with string key
    ctx = {'x': 3}
    norm = g.normalize_context(ctx.copy())
    assert op in norm
    # context not a mapping
    with pytest.raises(ValueError):
        g.normalize_context([('x', 3)])
    # context duplicate keys
    ctx_dup = {op: 1, 'x': 2}
    with pytest.raises(ValueError):
        g.normalize_context(ctx_dup.copy())

def test_graph_normalize_context_kwargs():
    g = Graph()
    op = DummyOp(name='x', graph=g)
    g.operations['x'] = op
    norm = g.normalize_context({}, x=99)
    assert op in norm and norm[op] == 99