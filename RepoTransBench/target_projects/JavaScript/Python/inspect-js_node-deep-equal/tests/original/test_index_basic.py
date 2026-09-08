from src.deep_equal import deep_equal

def test_primitive_equal():
    assert deep_equal(1, 1)
    assert deep_equal('a', 'a')
    assert deep_equal(True, True)

def test_primitive_not_equal():
    assert not deep_equal(1, 2)
    assert not deep_equal('a', 'b')
    assert not deep_equal(True, False)

def test_object_equal():
    assert deep_equal({'a': 1}, {'a': 1})

def test_object_not_equal():
    assert not deep_equal({'a': 1}, {'b': 1})
    assert not deep_equal({'a': 1}, {'a': 2})

def test_array_equal():
    assert deep_equal([1, 2, 3], [1, 2, 3])

def test_array_not_equal():
    assert not deep_equal([1, 2, 3], [1, 2])
    assert not deep_equal([1, 2, 3], [3, 2, 1])