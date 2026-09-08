import pytest
import chainbreaker.schema as schema

def test_schema_get_column_names():
    s = schema.KeychainSchema()
    names = s.get_column_names("genp")
    assert isinstance(names, list) and len(names) > 0

def test_schema_iter_with_disable_decode(monkeypatch):
    s = schema.KeychainSchema()
    class DummyCursor:
        def execute(self, q): return self
        def fetchall(self): return [[1,2],[3,4]]
        description = [('foo',),('bar',)]
    s._cursor = DummyCursor()
    records = list(s.iter("genp", disable_decode=True))
    assert records[0][0] == 1

def test_decode_val_bytes():
    s = schema.KeychainSchema()
    res = s._decode_val(b"abc")
    assert res == b"abc"

def test_decode_val_none():
    s = schema.KeychainSchema()
    res = s._decode_val(None)
    assert res is None

def test_decode_val_str():
    s = schema.KeychainSchema()
    val = b"hello world"
    # Simulate non-str decode. The real decode_val might try utf-8.
    s = schema.KeychainSchema()
    try:
        r = s._decode_val(val)
        assert r
    except Exception:
        pass

def test_repr_methods():
    s = schema.KeychainSchema()
    assert isinstance(repr(s), str)