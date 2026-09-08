from src.deep_equal import deep_equal

def test_circular_references_equal():
    obj1 = {}
    obj1['self'] = obj1
    obj2 = {}
    obj2['self'] = obj2
    assert deep_equal(obj1, obj2)

def test_circular_references_not_equal():
    obj1 = {}
    obj1['self'] = obj1
    obj2 = {}
    assert not deep_equal(obj1, obj2)