from src.deep_equal import deep_equal

def test_circular_references_equal_different_property_name():
    obj1 = {}
    obj1['loop'] = obj1
    obj2 = {}
    obj2['loop'] = obj2
    assert deep_equal(obj1, obj2)

def test_circular_references_not_equal_different_structure():
    obj1 = {}
    obj1['foo'] = obj1
    obj2 = {}
    obj2['foo'] = {}
    assert not deep_equal(obj1, obj2)