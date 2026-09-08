import os
import pickle
import zipfile
import tempfile
import pytest
import types

import src.ai_models.checkpoint as checkpoint

# Mocks for torch and UntypedStorage (for environments without torch)
class FakeTorch:
    float32 = "float32"
    class UntypedStorage:
        def __init__(self, v):
            self.v = v

def test_tidy_dict_and_list_tuple():
    d = {"a": [1, 2, {"b": (3, None)}], "c": (4, 5)}
    assert checkpoint.tidy(d) == {'a': [1, 2, {'b': (3, None)}], 'c': (4, 5)}

def test_tidy_base_types():
    for val in [None, 3, 0.1, "foo", True]:
        assert checkpoint.tidy(val) == val

def test_tidy_unknown_type():
    class Foo: pass
    f = Foo()
    assert checkpoint.tidy(f) == f

def test_FakeStorage_construction(monkeypatch):
    # Patch torch for environments where it's not installed
    monkeypatch.setitem(__import__("sys").modules, "torch", FakeTorch)
    s = checkpoint.FakeStorage()
    assert hasattr(s, 'dtype')
    assert hasattr(s, '_untyped_storage')

def test_UnpicklerWrapper(monkeypatch):
    data = pickle.dumps("abc")
    f = types.SimpleNamespace()
    f.read = lambda n=-1: data
    f.readable = lambda: True
    f.readline = lambda: b""
    # monkeypatch torch
    monkeypatch.setitem(__import__("sys").modules, "torch", FakeTorch)
    uw = checkpoint.UnpicklerWrapper(data)
    # Can't call load on bytes directly; test persistent_load
    res = uw.persistent_load("id")
    assert isinstance(res, checkpoint.FakeStorage)

def make_zip_with_data_pkl(obj, filename="data.pkl", extra=False):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(temp, "w") as zf:
        # data.pkl as requested
        zf.writestr(filename, pickle.dumps(obj))
        if extra:
            zf.writestr("data2.pkl", b"data2")
    temp.close()
    return temp.name

def test_peek_single_data_pkl(monkeypatch):
    # Patch torch for storage creation
    monkeypatch.setitem(__import__("sys").modules, "torch", FakeTorch)
    obj = {'foo': 1}
    zfile = make_zip_with_data_pkl(obj)
    result = checkpoint.peek(zfile)
    assert isinstance(result, dict) and result['foo'] == 1
    os.unlink(zfile)

def test_peek_duplicate_data_pkl(monkeypatch):
    monkeypatch.setitem(__import__("sys").modules, "torch", FakeTorch)
    # Simulate two "data.pkl" files by adding them with different paths
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(temp, "w") as zf:
        zf.writestr("first/data.pkl", pickle.dumps({'x': 1}))
        zf.writestr("second/data.pkl", pickle.dumps({'y': 2}))
    temp.close()
    with pytest.raises(Exception) as excinfo:
        checkpoint.peek(temp.name)
    assert "Found two data.pkl" in str(excinfo.value)
    os.unlink(temp.name)