from src import frozen

def test_not_refreeze_already_frozen_arrays():
    arr = [2, 3]
    froz1 = frozen.freeze(arr)
    froz2 = frozen.freeze(froz1)
    assert froz1 is froz2

def test_tojs_on_string_and_boolean_primitives():
    assert frozen.toJS("test") == "test"
    assert frozen.toJS(False) is False
    assert frozen.toJS(None) is None

def test_equals_custom_equals_returns_true():
    class CustomType:
        def equals(self, other):
            return True
    a = CustomType()
    b = CustomType()
    assert frozen.equals(a, b) is True

def test_equals_for_self_referencing_arrays():
    a = []
    a.append(a)
    b = []
    b.append(b)
    assert frozen.equals(a, b) is True

def test_cyclic_check_with_different_primitives():
    assert frozen.equals("abc", "abc") is True