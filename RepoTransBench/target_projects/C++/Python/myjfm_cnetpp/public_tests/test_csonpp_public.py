import pytest

class CsonObject:
    kArray = 'array'
    def __init__(self):
        self.d = {}
        self.arr = []
        self._type = 'object'

    def __setitem__(self, k, v):
        self.d[k] = v

    def __getitem__(self, k):
        return CsonValue(self.d[k])

    def SetType(self, type_):
        if type_ == self.kArray:
            self._type = type_
            self.arr = []

    def Append(self, v):
        self.arr.append(v)

    def Count(self):
        return len(self.arr)

class CsonValue:
    def __init__(self, v):
        self._v = v

    def AsString(self):
        return self._v if isinstance(self._v, str) else str(self._v)

    def AsInt(self):
        return self._v if isinstance(self._v, int) else int(self._v)

def test_string_and_int():
    obj = CsonObject()
    obj["pkey"] = "publicvalue"
    obj["pnum"] = 888
    assert obj["pkey"].AsString() == "publicvalue"
    assert obj["pnum"].AsInt() == 888

def test_nested_array():
    arr = CsonObject()
    arr.SetType(CsonObject.kArray)
    arr.Append(3)
    arr.Append(7)
    arr.Append(9)
    assert arr.Count() == 3
    assert arr.arr[1] == 7