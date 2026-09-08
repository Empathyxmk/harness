from src import frozen

def test_freeze_object_and_keep_properties_public():
    obj = {'p': 6, 'q': "hi"}
    fz = frozen.freeze(obj)
    assert fz['p'] == 6
    assert fz['q'] == "hi"
    assert getattr(fz, '_is_frozen', False) is True or hasattr(fz, '_frozen')

def test_freeze_array_and_keep_values_public():
    arr = [7, 11]
    fz = frozen.freeze(arr)
    assert isinstance(fz, list)
    assert fz[1] == 11
    assert getattr(fz, '_is_frozen', False) is True or hasattr(fz, '_frozen')

def test_tojs_returns_unfrozen_js_structures_public():
    fz = frozen.freeze({'u': 1, 'v': [9, 10]})
    val = frozen.toJS(fz)
    assert val == {'u': 1, 'v': [9, 10]}

def test_equals_returns_true_for_deep_equal_plain_objects_public():
    assert frozen.equals({'x': 1, 'y': 2}, {'x': 1, 'y': 2}) is True

def test_equals_returns_false_for_different_plain_objects_public():
    assert frozen.equals({'x': 99}, {'z': 99}) is False