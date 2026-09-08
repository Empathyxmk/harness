import pytest

class ResultSetMock:
    def __init__(self, val):
        self._val = val
    def getString(self, colname):
        return self._val

class StringListConverter:
    def __init__(self):
        pass

    def getFieldValueFromResultSet(self, rs, col):
        s = rs.getString(col)
        if s is None:
            return []
        out = []
        buff = ""
        i = 0
        while i < len(s):
            if s[i] == "\\":
                if i + 1 < len(s):
                    buff += s[i+1]
                    i += 2
                else:
                    buff += "\\"
                    i += 1
            elif s[i] == ",":
                out.append(buff)
                buff = ""
                i += 1
            else:
                buff += s[i]
                i += 1
        out.append(buff)
        return out

    def convertFieldValueToColumn(self, list_):
        if list_ is None or list_ == []:
            return ""
        s = []
        for val in list_:
            v = val.replace("\\", "\\\\").replace(",", "\\,")
            s.append(v)
        return ",".join(s)

def assert_convert(converter, s, list_):
    rs = ResultSetMock(s)
    assert converter.getFieldValueFromResultSet(rs, "columnName") == list_
    assert converter.convertFieldValueToColumn(list_) == s

def test_all():
    list_ = []
    converter = StringListConverter()
    assert_convert(converter, "", list_)

    list_.append("foo")
    assert_convert(converter, "foo", list_)

    list_.append("bar")
    assert_convert(converter, "foo,bar", list_)

    list_.append("b\\a,z")
    assert_convert(converter, "foo,bar,b\\\\a\\,z", list_)

def test_null_results_in_empty_list():
    rs = ResultSetMock(None)
    converter = StringListConverter()
    value = converter.getFieldValueFromResultSet(rs, "columnName")
    assert value is not None
    assert len(value) == 0