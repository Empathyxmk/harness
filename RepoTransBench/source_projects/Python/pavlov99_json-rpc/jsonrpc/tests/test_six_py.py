import sys
import types
import pytest
import jsonrpc.six as six

def test_py_version_constants():
    assert (six.PY2 or six.PY3) is True

def test_string_types():
    # Python 3: str, Python 2: basestring
    if six.PY3:
        assert isinstance("abc", six.string_types)
        assert not isinstance(b"abc", six.string_types)
    else:
        assert isinstance(u"abc", six.string_types)
        assert isinstance("abc", six.string_types)

def test_integer_types():
    assert isinstance(42, six.integer_types)

def test_text_binary_types():
    txt = six.text_type("abc")
    bin_type = six.binary_type(b"abc")
    assert isinstance(txt, six.text_type)
    assert isinstance(bin_type, six.binary_type)

def test_maxsize_value():
    # Just check it's an int and > 1000
    assert isinstance(six.MAXSIZE, int)
    assert six.MAXSIZE > 1000

def test_add_doc():
    def foo(): pass
    six._add_doc(foo, "my doc")
    assert foo.__doc__ == "my doc"

def test_import_module():
    mod = six._import_module("json")
    import json
    assert mod is json

def test_lazy_descr_resolves_once(monkeypatch):
    class DummyType(object): pass
    dummy = DummyType()
    value = []
    class MyLazy(six._LazyDescr):
        def _resolve(self):
            value.append(1)
            return "bar"
    MyLazyField = MyLazy("foo")
    setattr(DummyType, "foo", MyLazyField)
    assert dummy.foo == "bar"
    assert dummy.foo == "bar"
    assert value == [1] # _resolve once

def test_moved_module(monkeypatch):
    class DummyType: pass
    moved = six.MovedModule("json", "json", "json")
    DummyType.json = moved
    inst = DummyType()
    assert inst.json is sys.modules["json"]

def test_moved_attribute(monkeypatch):
    class DummyType: pass
    moved = six.MovedAttribute("loads", "json", "json", "loads", "loads")
    DummyType.loads = moved
    inst = DummyType()
    import json
    assert inst.loads == json.loads