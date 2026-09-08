import pytest

class Bundle(dict):
    def __init__(self):
        super().__init__()
        self._arraylist = None

    def putParcelableArrayList(self, key, value):
        self._arraylist = value

    def getParcelableArrayList(self, key):
        return self._arraylist

class Parcelable:
    pass

class DummyParcelable(Parcelable):
    def __eq__(self, other):
        return isinstance(other, DummyParcelable)

    def __hash__(self):
        return 0

class CastedArrayListArgsBundler:
    def put(self, key, value, bundle):
        if not isinstance(value, list):
            raise TypeError("Value must be a list")
        bundle.putParcelableArrayList(key, value)

    def get(self, key, bundle):
        return bundle.getParcelableArrayList(key)

def test_put_throws_if_not_arraylist():
    bundler = CastedArrayListArgsBundler()
    value = (DummyParcelable(), DummyParcelable())
    with pytest.raises(TypeError):
        bundler.put("key", value, Bundle())

def test_put_and_get_with_arraylist():
    bundler = CastedArrayListArgsBundler()
    arr_list = [DummyParcelable(), DummyParcelable()]
    bundle = Bundle()
    bundler.put("key", arr_list, bundle)
    result = bundler.get("key", bundle)
    assert arr_list == result