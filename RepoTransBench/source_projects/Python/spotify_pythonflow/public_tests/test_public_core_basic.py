import pytest
from pythonflow.core import Graph, Operation

class DummyOp(Operation):
    # minimal operation for testing graph
    def _evaluate(self):
        return 100

def test_graph_enter_exit_public():
    g = Graph()
    assert getattr(g._globals, 'default_graph', None) is None
    with g:
        assert Graph._globals.default_graph is g
    assert getattr(g._globals, 'default_graph', None) is None

def test_graph_duplicate_enter_public():
    g = Graph()
    with g:
        with pytest.raises(AssertionError):
            with g:
                pass

def test_graph_normalize_operation_with_instance_public():
    g = Graph()
    op = DummyOp(name="foo", graph=g)
    g.operations["foo"] = op
    assert g.normalize_operation(op) is op
    # Bad graph
    other = Graph()
    op2 = DummyOp(name="bar", graph=other)
    with pytest.raises(RuntimeError):
        g.normalize_operation(op2)

def test_graph_normalize_operation_with_name_public():
    g = Graph()
    op = DummyOp(name="test", graph=g)
    g.operations["test"] = op
    assert g.normalize_operation("test") is op

def test_graph_normalize_operation_invalid_public():
    g = Graph()
    with pytest.raises(ValueError):
        g.normalize_operation(None)
    with pytest.raises(KeyError):
        g.normalize_operation("unknown_operation")

def test_graph_normalize_context_and_duplicates_public():
    g = Graph()
    op = DummyOp(name='y', graph=g)
    g.operations['y'] = op
    # context with string key
    ctx = {'y': 8}
    norm = g.normalize_context(ctx.copy())
    assert op in norm
    # context not a mapping
    with pytest.raises(ValueError):
        g.normalize_context([('y', 8)])
    # context duplicate keys
    ctx_dup = {op: 2, 'y': 5}
    with pytest.raises(ValueError):
        g.normalize_context(ctx_dup.copy())

def test_graph_normalize_context_kwargs_public():
    g = Graph()
    op = DummyOp(name='z', graph=g)
    g.operations['z'] = op
    norm = g.normalize_context({}, z=123)
    assert op in norm and norm[op] == 123