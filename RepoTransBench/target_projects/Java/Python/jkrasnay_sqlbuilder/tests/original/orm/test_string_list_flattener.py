import pytest

class StringListFlattener:
    def __init__(self):
        self.convert_empty_to_null = False

    def set_convert_empty_to_null(self, val):
        self.convert_empty_to_null = val
        return self

    def join(self, list_):
        if list_ is None:
            if self.convert_empty_to_null:
                return None
            return ""
        s = []
        for val in list_:
            if val is None:
                raise ValueError("IllegalArgumentException")
            v = val.replace("\\", "\\\\").replace(",", "\\,")
            s.append(v)
        return ",".join(s)

    def split(self, flattened):
        if flattened is None:
            return []
        if flattened == "":
            return [""]
        out = []
        buff = ""
        i = 0
        while i < len(flattened):
            if flattened[i] == "\\":
                if i + 1 < len(flattened):
                    buff += flattened[i + 1]
                    i += 2
                else:
                    buff += "\\"
                    i += 1
            elif flattened[i] == ",":
                out.append(buff)
                buff = ""
                i += 1
            else:
                buff += flattened[i]
                i += 1
        out.append(buff)
        return out

def assert_equivalent(list_, flattened):
    slf = StringListFlattener()
    assert slf.join(list_) == flattened
    assert slf.split(flattened) == list_

def test_all():
    slf = StringListFlattener()
    list_ = slf.split(None)
    assert list_ is not None
    assert len(list_) == 0

    list_ = []
    assert_equivalent(list_, "")

    list_.append(None)
    with pytest.raises(ValueError):
        slf.join(list_)

    list_.clear()
    list_.append("foo")
    assert_equivalent(list_, "foo")

    list_.append("bar")
    assert_equivalent(list_, "foo,bar")

    list_.append("b\\a,z")
    assert_equivalent(list_, "foo,bar,b\\\\a\\,z")

    list_.append("quux")
    assert_equivalent(list_, "foo,bar,b\\\\a\\,z,quux")

    list_.clear()
    list_.extend(["", "", ""])
    assert_equivalent(list_, ",,")

def test_convert_empty_to_null():
    slf = StringListFlattener().set_convert_empty_to_null(True)
    list_ = slf.split(None)
    assert list_ is not None
    assert len(list_) == 0

    list_ = []
    assert_equivalent(list_, "")

    list_.append(None)
    assert slf.join(list_) == ""

    list_.append(None)
    assert slf.join(list_) == ","

    list2 = slf.split(",")
    assert len(list2) == 2
    assert list2[0] is not None or list2[0] is None
    assert list2[1] is not None or list2[1] is None