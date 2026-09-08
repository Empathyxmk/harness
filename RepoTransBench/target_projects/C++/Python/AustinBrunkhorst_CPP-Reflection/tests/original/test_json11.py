import pytest

class JsonType:
    NUL = 0
    NUMBER = 1
    BOOL = 2
    STRING = 3
    ARRAY = 4
    OBJECT = 5

class Json:
    def __init__(self, value=None):
        self._v = value
        if value is None:
            self._type = JsonType.NUL
        elif isinstance(value, bool):
            self._type = JsonType.BOOL
        elif isinstance(value, (int, float)):
            self._type = JsonType.NUMBER
        elif isinstance(value, str):
            self._type = JsonType.STRING
        elif isinstance(value, list):
            self._type = JsonType.ARRAY
            self._v = [Json(x) if not isinstance(x, Json) else x for x in value]
        elif isinstance(value, dict):
            self._type = JsonType.OBJECT
            self._v = {k: (v if isinstance(v, Json) else Json(v)) for k, v in value.items()}
        else:
            self._type = JsonType.NUL

    def is_null(self):
        return self._type == JsonType.NUL

    def type(self):
        return self._type

    def number_value(self):
        return float(self._v) if self._type == JsonType.NUMBER else 0.0

    def bool_value(self):
        return bool(self._v) if self._type == JsonType.BOOL else False

    def string_value(self):
        return self._v if self._type == JsonType.STRING else ""

    def __getitem__(self, key):
        if self._type == JsonType.ARRAY and isinstance(key, int):
            return self._v[key]
        if self._type == JsonType.OBJECT and isinstance(key, str):
            return self._v.get(key, Json())
        return Json()

    @staticmethod
    def parse(text, err_out):
        import json as pyjson
        try:
            val = pyjson.loads(text)
            err_out.clear()
            return Json._py_to_json(val)
        except Exception as e:
            err_out.append(str(e))
            return Json()

    @staticmethod
    def _py_to_json(val):
        if val is None:
            return Json()
        elif isinstance(val, bool):
            return Json(val)
        elif isinstance(val, (int, float)):
            return Json(float(val))
        elif isinstance(val, str):
            return Json(val)
        elif isinstance(val, list):
            return Json([Json._py_to_json(v) for v in val])
        elif isinstance(val, dict):
            return Json({k: Json._py_to_json(v) for k, v in val.items()})
        return Json()

    def __eq__(self, other):
        if not isinstance(other, Json):
            return False
        if self._type != other._type:
            return False
        if self._type == JsonType.ARRAY:
            return self._v == other._v
        if self._type == JsonType.OBJECT:
            return self._v == other._v
        return self._v == other._v

def test_null_type():
    j = Json()
    assert j.is_null()
    assert j.type() == JsonType.NUL

def test_number_type():
    j = Json(3.14)
    assert j.number_value() == 3.14
    assert j.type() == JsonType.NUMBER

def test_bool_type():
    j = Json(True)
    assert j.bool_value()
    assert j.type() == JsonType.BOOL

def test_string_type():
    j = Json("hello")
    assert j.string_value() == "hello"
    assert j.type() == JsonType.STRING

def test_array_type():
    v = [Json(1), Json(2)]
    j = Json(v)
    assert j[0] == Json(1)
    assert j[1] == Json(2)
    assert j.type() == JsonType.ARRAY

def test_object_type():
    m = {"a": 1, "b": 2}
    j = Json(m)
    assert j["a"] == Json(1)
    assert j["b"] == Json(2)
    assert j.type() == JsonType.OBJECT

def test_parse_valid():
    err = []
    j = Json.parse('{"a":2, "b":null}', err)
    assert not err
    assert j["a"] == Json(2)
    assert j["b"].is_null()

def test_parse_invalid():
    err = []
    j = Json.parse("{bad json}", err)
    assert err
    assert j.is_null()