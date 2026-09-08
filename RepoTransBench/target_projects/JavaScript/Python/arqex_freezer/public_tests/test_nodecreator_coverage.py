from src import nodeCreator

def test_create_frozen_array_public():
    arr = nodeCreator.createNode([100, 200])
    assert isinstance(arr, list)
    assert arr[0] == 100
    # Python doesn't have Object.isFrozen, assume frozen-ness by some marker or method
    assert getattr(arr, '_is_frozen', False) is True or hasattr(arr, '_frozen')

def test_create_frozen_object_public():
    obj = nodeCreator.createNode({'foo': 7, 'bar': 8})
    assert isinstance(obj, dict)
    assert obj['foo'] == 7
    assert getattr(obj, '_is_frozen', False) is True or hasattr(obj, '_frozen')

def test_return_primitives_as_is_public():
    assert nodeCreator.createNode("sample") == "sample"
    assert nodeCreator.createNode(555) == 555
    assert nodeCreator.createNode(False) is False