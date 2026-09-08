import pytest
import json

class Bean:
    def __init__(self, field1=None, field2=None):
        self.field1 = field1
        self.field2 = field2

    def __eq__(self, other):
        return (
            isinstance(other, Bean)
            and self.field1 == other.field1
            and self.field2 == other.field2
        )

class JsonUtil:
    @staticmethod
    def Str2JsonBean(json_str, cls):
        try:
            d = json.loads(json_str)
            return cls(**d)
        except Exception:
            return None

    @staticmethod
    def JsonBean2Str(bean):
        if bean is None:
            return "null"
        try:
            return json.dumps(bean.__dict__, sort_keys=True)
        except Exception:
            return None

    @staticmethod
    def JsonList2Str(lst):
        if not lst:
            return None
        try:
            return json.dumps([obj.__dict__ for obj in lst], sort_keys=True)
        except Exception:
            return None

def test_str2jsonbean_valid_json():
    json_str = '{"field1":"test","field2":123}'
    bean = JsonUtil.Str2JsonBean(json_str, Bean)
    assert bean is not None
    assert bean.field1 == "test"
    assert bean.field2 == 123

def test_str2jsonbean_invalid_json():
    json_str = '{field1:test,field2:abc}'
    bean = JsonUtil.Str2JsonBean(json_str, Bean)
    assert bean is None

def test_jsonbean2str_valid():
    bean = Bean("abc", 42)
    json_str = JsonUtil.JsonBean2Str(bean)
    assert json_str is not None
    assert '"field1": "abc"' in json_str or '"field1":"abc"' in json_str
    assert '"field2": 42' in json_str or '"field2":42' in json_str

def test_jsonbean2str_null():
    json_null = JsonUtil.JsonBean2Str(None)
    assert json_null == "null"

def test_jsonlist2str_empty_list():
    res = JsonUtil.JsonList2Str([])
    assert res is None

def test_jsonlist2str_multiple():
    b1 = Bean("a", 1)
    b2 = Bean("b", 2)
    res = JsonUtil.JsonList2Str([b1, b2])
    assert res is not None
    assert res.startswith("[")
    assert res.endswith("]")
    assert '"field1": "a"' in res or '"field1":"a"' in res
    assert '"field1": "b"' in res or '"field1":"b"' in res
    assert "," in res