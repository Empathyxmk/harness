import pytest
import json

from scrapy_jsonrpc import serialize

def test_scrapy_json_dumps_basic():
    assert serialize.scrapy_json_dumps({"a": 1, "b": 2}) == '{"a": 1, "b": 2}' or serialize.scrapy_json_dumps({"a": 1, "b": 2}) == '{"b": 2, "a": 1}'

def test_scrapy_json_dumps_handles_custom_item():
    class MyItem(serialize.BaseItem): pass
    i = MyItem(a=5)
    s = serialize.scrapy_json_dumps(i)
    assert '"a": 5' in s

def test_scrapy_json_dumps_handles_field():
    f = serialize.Field()
    s = serialize.scrapy_json_dumps({"f": f})
    assert '"<Field instance>"' in s

def test_scrapy_json_dumps_handles_fake_spider():
    class Spider:
        name = "sp1"
    sp = Spider()
    d = {"sp": sp}
    s = serialize.scrapy_json_dumps(d)
    assert '"<Spider: sp1>"' in s

def test_scrapy_json_loads_and_decoder():
    d = {"a": 1, "b": "hi"}
    s = serialize.scrapy_json_dumps(d)
    loaded = serialize.scrapy_json_loads(s)
    assert loaded == d

def test_default_typeerror():
    class NotSerializable: pass
    with pytest.raises(TypeError):
        serialize.scrapy_json_dumps(NotSerializable())

def test_is_item():
    assert serialize.is_item({"x": 1})
    class It(serialize.BaseItem): pass
    assert serialize.is_item(It())
    assert not serialize.is_item(123)
    assert not serialize.is_item("str")