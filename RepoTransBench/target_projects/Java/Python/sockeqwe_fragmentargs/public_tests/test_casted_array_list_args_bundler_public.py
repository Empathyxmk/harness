from tests.original.test_casted_array_list_args_bundler import Bundle, CastedArrayListArgsBundler
import pytest

class MyParcelablePublic:
    def __init__(self, str_):
        self.str = str_

    def __eq__(self, other):
        return isinstance(other, MyParcelablePublic) and self.str == other.str

    def __hash__(self):
        return hash(self.str)

def test_casted_array_list_args_bundler_with_parcelable_public_variant():
    bundler = CastedArrayListArgsBundler()
    data = [MyParcelablePublic("dragonfruit"), MyParcelablePublic("peach"), MyParcelablePublic("plum")]
    bundle = Bundle()
    bundler.put("UniqueFruitKey", data, bundle)
    restored = bundler.get("UniqueFruitKey", bundle)
    assert data == restored