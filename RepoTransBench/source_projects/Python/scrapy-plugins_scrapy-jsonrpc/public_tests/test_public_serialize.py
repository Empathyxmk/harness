import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapy_jsonrpc import serialize

def test_public_json_dumps_and_loads():
    orig = {"c": 100, "test": [1, 7, 8]}
    encoded = serialize.json_dumps(orig)
    decoded = serialize.json_loads(encoded)
    assert decoded == orig

def test_public_repr_loads_and_dumps():
    orig = [11, {"foo": "bar"}, (3, 4)]
    dumped = serialize.repr_dumps(orig)
    loaded = serialize.repr_loads(dumped)
    assert loaded == orig

def test_public_repr_dumps_handles_none():
    val = None
    dumped = serialize.repr_dumps(val)
    loaded = serialize.repr_loads(dumped)
    assert loaded is None

def test_public_unicode_and_utf8():
    # Testing unicode/str and utf-8 string encoding/decoding
    s_unicode = "üñîçødê"
    utf8ed = serialize.to_utf8(s_unicode)
    assert isinstance(utf8ed, bytes)
    assert utf8ed.decode("utf-8") == s_unicode

    s_bytes = "测试".encode("utf-8")
    s_str = serialize.to_unicode(s_bytes)
    assert isinstance(s_str, str)
    assert s_str == "测试"