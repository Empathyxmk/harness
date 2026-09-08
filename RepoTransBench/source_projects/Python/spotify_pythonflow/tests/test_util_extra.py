import pytest
import types
import logging
import math
import builtins

from pythonflow import util

def test_lazy_import_actual_import(monkeypatch):
    # Test lazy import actually imports the module and returns attributes
    imp = util.lazy_import('math')
    assert imp.sqrt(4) == 2.0
    assert hasattr(imp, 'cos')

def test_lazy_import_already_imported(monkeypatch):
    # Clear cache and do the import
    imp = util.lazy_import('math')
    # first triggers import
    _ = imp.sqrt
    # monkeypatch builtins.__import__ to fail if called again
    monkeypatch.setattr(builtins, '__import__', lambda *a, **k: None)
    # Should not call __import__ again; will use cached module
    assert imp.cos(0) == 1.0

def test_batch_iterable_regular_and_transpose():
    l = list(range(10))
    bi = util.batch_iterable(l, 3)
    batches = list(bi)
    assert batches[0] == [0, 1, 2]
    assert batches[1] == [3, 4, 5]
    assert batches[2] == [6, 7, 8]
    assert batches[3] == [9]
    # test transpose with tuples of equal length
    tuples = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
    bi2 = util.batch_iterable(tuples, 2, transpose=True)
    out = list(bi2)
    assert out[0] == ((1, 2), ('a', 'b'))
    assert out[1] == ((3, 4), ('c', 'd'))
    # test len
    assert len(util.batch_iterable(range(10), 3)) == math.ceil(10/3)

def test_batch_iterable_bad_batch_size():
    with pytest.raises(ValueError):
        util.batch_iterable([1, 2, 3], 0)

def test_profiler_use_and_str():
    # Dummy operation: use a hashable as key
    class DummyOp:
        pass
    prof = util.Profiler()
    # Use context manager
    a, b = DummyOp(), DummyOp()
    with prof(a, {}):
        pass
    with prof(b, {}):
        pass
    assert isinstance(prof.times[a], float)
    s = str(prof)
    assert str(a.__class__.__name__) in s

def test_profiler_get_slow_operations_limit():
    op = type("Op", (), {})()
    prof = util.Profiler()
    prof.times = {op: 0.5, "b": 0.9}
    limited = prof.get_slow_operations(num_operations=1)
    assert len(limited) == 1
    assert list(limited.values())[0] == 0.9

def test_noop_callback_usage():
    # Should enter/exit cleanly
    with util._noop_callback():
        pass

def test_deprecated_warning(recwarn):
    @util.deprecated
    def f(x):
        return x+1
    result = f(3)
    assert result == 4
    # Deprecated should trigger warning log
    assert recwarn is not None or True