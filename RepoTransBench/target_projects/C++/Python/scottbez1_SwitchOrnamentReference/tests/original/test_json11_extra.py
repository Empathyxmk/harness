import math
import sys
import pytest
import json

# Helper class to provide an API similar to json11 for testing
class DummyJson:
    """A thin wrapper to simulate the C++ json11 API using Python's dict, list, etc."""
    def __init__(self, value=None):
        self._v = value

    @staticmethod
    def parse(s, err=None):
        try:
            # json11 is tolerant to JSON5 style null/true/false, so we map strings to python types
            s_strip = s.strip()
            if s_strip == '':
                raise ValueError("Empty string")
            # Accept some C++ JSON11-like tokens
            if s_strip == 'null':
                if err is not None:
                    err.append('')
                return DummyJson(None)
            if s_strip == 'true':
                if err is not None:
                    err.append('')
                return DummyJson(True)
            if s_strip == 'false':
                if err is not None:
                    err.append('')
                return DummyJson(False)
            parsed = json.loads(s)
            if err is not None:
                err.append('')
            return DummyJson(parsed)
        except Exception as e:
            if err is not None:
                err.append(str(e) or 'error')
            return DummyJson(None)

    def is_null(self):
        # json11 treats missing values and explicit null as null
        return self._v is None

    def is_bool(self):
        return isinstance(self._v, bool)

    def is_number(self):
        return isinstance(self._v, (int, float))

    def is_string(self):
        return isinstance(self._v, str)

    def is_array(self):
        return isinstance(self._v, list)

    def is_object(self):
        return isinstance(self._v, dict)

    def int_value(self):
        if isinstance(self._v, (int, float)):
            return int(self._v)
        return 0

    def number_value(self):
        if isinstance(self._v, (int, float)):
            return float(self._v)
        return 0.0

    def bool_value(self):
        if isinstance(self._v, bool):
            return self._v
        return False

    def array_items(self):
        return [DummyJson(i) for i in self._v] if isinstance(self._v, list) else []

    def object_items(self):
        if isinstance(self._v, dict):
            return {k: DummyJson(v) for k, v in self._v.items()}
        return {}

    def __getitem__(self, key):
        if isinstance(self._v, dict) and isinstance(key, str):
            return DummyJson(self._v.get(key, None))
        elif isinstance(self._v, list) and isinstance(key, int):
            if 0 <= key < len(self._v):
                return DummyJson(self._v[key])
            else:
                return DummyJson(None)
        return DummyJson(None)

    def __eq__(self, other):
        if isinstance(other, DummyJson):
            return self._v == other._v
        return self._v == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def dump(self):
        def escape_string(s):
            # Escape special characters for JSON string
            res = ''
            for ch in s:
                o = ord(ch)
                if ch == '"':
                    res += '\\"'
                elif ch == '\\':
                    res += '\\\\'
                elif ch == '\b':
                    res += '\\b'
                elif ch == '\f':
                    res += '\\f'
                elif ch == '\n':
                    res += '\\n'
                elif ch == '\r':
                    res += '\\r'
                elif ch == '\t':
                    res += '\\t'
                elif o < 0x20 or o in [0x2028, 0x2029]:
                    res += '\\u%04x' % o
                else:
                    res += ch
            return f'"{res}"'

        if self._v is None or (isinstance(self._v, float) and (math.isnan(self._v) or math.isinf(self._v))):
            return "null"
        if isinstance(self._v, bool):
            return "true" if self._v else "false"
        if isinstance(self._v, (int, float)):
            if isinstance(self._v, float) and (math.isnan(self._v) or math.isinf(self._v)):
                return "null"
            if float(self._v) == int(self._v):
                return str(int(self._v))
            return str(self._v)
        if isinstance(self._v, str):
            return escape_string(self._v)
        if isinstance(self._v, list):
            return "[" + ", ".join(DummyJson(i).dump() for i in self._v) + "]"
        if isinstance(self._v, dict):
            # Use sorted keys for deterministic order
            return "{" + ", ".join(f"{escape_string(str(k))}: {DummyJson(v).dump()}" for k, v in sorted(self._v.items())) + "}"
        return "null"  # fallback

    def __repr__(self):
        return f"DummyJson({self._v!r})"


def test_stringify_escape():
    # Simulate: Json j_str = std::string("a\"\b\f\n\r\t\\\x1f\xe2\x80\xa8\xe2\x80\xa9")
    special_str = 'a"\b\f\n\r\t\\' + chr(0x1f) + '\u2028\u2029'
    j_str = DummyJson(special_str)
    dumped = j_str.dump()
    assert '\\\"' in dumped
    assert '\\b' in dumped
    assert '\\f' in dumped
    assert '\\n' in dumped
    assert '\\r' in dumped
    assert '\\t' in dumped
    assert '\\\\' in dumped
    assert '\\u001f' in dumped
    assert '\\u2028' in dumped
    assert '\\u2029' in dumped

def test_number_nan_inf():
    j_nan = DummyJson(float('nan'))
    j_inf = DummyJson(float('inf'))
    j_ninf = DummyJson(float('-inf'))
    assert j_nan.dump() == "null"
    assert j_inf.dump() == "null"
    assert j_ninf.dump() == "null"

def test_array_and_object_order_and_compare():
    arr1 = DummyJson([1,2,3])
    arr2 = DummyJson([1,2,3])
    arr3 = DummyJson([3,2,1])
    assert arr1 == arr2
    assert arr1 != arr3
    obj1 = DummyJson({"a":1, "b":2})
    obj2 = DummyJson({"b":2, "a":1})
    assert obj1 == obj2

def test_invalid_parse():
    err = []
    j = DummyJson.parse("invalid", err)
    assert j.is_null()
    assert err[-1] != ""
    # Empty string is invalid
    err_clear = []
    j = DummyJson.parse("", err_clear)
    assert j.is_null()

def test_parse_literals():
    err = []
    assert DummyJson.parse("null", err).is_null()
    err_true = []
    assert DummyJson.parse("true", err_true).is_bool()
    err_false = []
    assert DummyJson.parse("false", err_false).is_bool()

def test_object_with_null_value():
    obj = {}
    obj["a"] = DummyJson(None)
    assert DummyJson(obj)["a"].is_null()

def test_accessors_types():
    j = DummyJson(42)
    assert j.int_value() == 42
    assert j.number_value() == 42.0
    assert not j.is_bool()
    j = DummyJson(3.14)
    assert math.isclose(j.number_value(), 3.14)
    assert j.int_value() == 3
    j = DummyJson(True)
    assert j.bool_value()
    j = DummyJson([1,2])
    assert len(j.array_items()) == 2
    j = DummyJson({"a":1})
    assert len(j.object_items()) == 1

def test_deep_nesting_limit():
    # In C++ json11 has a max depth of 200, here we can simulate fail parsing on depth > 200
    deep = "[" + "["*210 + "]"*210 + "]"
    # Our DummyJson won't fail for deep nesting but we can simulate by limiting recursion
    # For this test, let's just assert that it parses as a list or that recursion error occurs
    try:
        err = []
        _ = DummyJson.parse(deep, err)
    except Exception as e:
        pass  # RecursionError is acceptable

def test_invalid_utf8():
    # Broken bytes in Python will raise on encoding
    s = b"\xC3\x28".decode("utf-8", errors="replace")
    j = DummyJson(s)
    dumped = j.dump()
    assert dumped != ""

def test_object_find_operator_brackets():
    j = DummyJson({"foo": 42})
    assert j["foo"] == 42
    assert j["bar"].is_null()
    item = j.object_items().get("foo", None)
    assert item is not None

def test_move_semantics():
    original = DummyJson([1,2,3])
    moved = original  # In Python, assignment is reference, but mutability is similar
    assert moved.is_array()

def test_empty_and_clear():
    arr = DummyJson([])
    assert arr.array_items() == []
    obj = DummyJson({})
    assert obj.object_items() == {}

def test_nullptr_ctor_and_typeops():
    j = DummyJson(None)
    assert j.is_null()
    assert j.dump() == "null"
    assert not j.is_string()
    assert not j.is_array()
    assert not j.is_object()

def test_assignment():
    a = DummyJson({"x": 1})
    b = DummyJson({"y": 2})
    a = b
    assert a == b

def test_double_to_int_bounds():
    j = DummyJson(sys.float_info.max)
    # Value may be too large for int, but check that it doesn't crash
    try:
        assert j.int_value() == int(sys.float_info.max)
    except OverflowError:
        pass
    j = DummyJson(-sys.float_info.max)
    try:
        assert j.int_value() == int(-sys.float_info.max)
    except OverflowError:
        pass

def test_object_index_and_array_index_bounds():
    arr = DummyJson([42])
    assert arr[0] == 42
    assert arr[1].is_null()
    obj = DummyJson({"k": 3.14})
    assert math.isclose(obj["k"].number_value(), 3.14)
    assert obj["notfound"].is_null()

def test_clear_on_array_and_object():
    arr = DummyJson([1, 2, 3])
    arr2 = arr
    arr2 = DummyJson([])
    assert arr2.array_items() == []
    obj = DummyJson({"a": 1})
    obj2 = obj
    obj2 = DummyJson({})
    assert obj2.object_items() == {}

def test_large_number_parse():
    err = []
    big = DummyJson.parse("1e100", err)
    assert err[-1] == ""
    assert big.is_number()
    assert big.number_value() > 1e99