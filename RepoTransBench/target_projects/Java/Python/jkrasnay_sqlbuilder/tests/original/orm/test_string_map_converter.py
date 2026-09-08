import pytest

class ResultSetMock:
    def __init__(self, val):
        self._val = val
    def getString(self, colname):
        return self._val

class StringMapConverter:
    def __init__(self):
        pass

    def getFieldValueFromResultSet(self, rs, col):
        s = rs.getString(col)
        if s is None:
            return {}
        result = {}
        for entry in s.split(","):
            if entry == "":
                continue
            pair = entry.split("=")
            key = pair[0]
            val = pair[1] if len(pair) > 1 else ""
            result[key] = val
        return result

    def convertFieldValueToColumn(self, map_):
        if map_ is None or map_ == {}:
            return ""
        items = []
        for k, v in map_.items():
            k_escaped = k.replace("\\", "\\\\").replace(",", "\\,")
            v_escaped = v.replace("\\", "\\\\").replace(",", "\\,")
            items.append(f"{k_escaped}={v_escaped}")
        return ",".join(items)

def assert_map_equals(expected, actual):
    assert len(expected) == len(actual)
    for k in expected:
        assert expected[k] == actual[k]

def assert_convert(converter, s, dict_):
    rs = ResultSetMock(s)
    assert_map_equals(dict_, converter.getFieldValueFromResultSet(rs, "columnName"))
    assert converter.convertFieldValueToColumn(dict_) == s

def test_all():
    map_ = {}
    converter = StringMapConverter()
    assert_convert(converter, "", map_)

    map_["foo"] = "bar"
    assert_convert(converter, "foo=bar", map_)

    map_["b\\a,z"] = "q\\uu,x"
    assert_convert(converter, "foo=bar,b\\a,z=q\\uu,x", map_)

def test_null_results_in_empty_map():
    rs = ResultSetMock(None)
    converter = StringMapConverter()
    value = converter.getFieldValueFromResultSet(rs, "columnName")
    assert value is not None
    assert len(value) == 0