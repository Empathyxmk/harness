from src.deep_equal import deep_equal

def test_primitives_booleans():
    assert deep_equal(True, True)
    assert not deep_equal(True, False)
    assert not deep_equal(False, 0)

def test_primitives_null_and_undefined():
    # In Python, None is null, and "undefined" JS semantics matches None for check.
    assert deep_equal(None, None)
    assert deep_equal(None, None)
    assert not deep_equal(None, 'undefined')  # strings vs None

def test_numbers():
    assert deep_equal(123, 123)
    assert not deep_equal(123, 321)
    assert not deep_equal(123, "123")

def test_strings():
    assert deep_equal('world', 'world')
    assert not deep_equal('world', 'WORLD')
    assert not deep_equal('world', 123)

def test_arrays():
    assert deep_equal([4, 5, 6], [4, 5, 6])
    assert not deep_equal([4, 5, 6], [6, 5, 4])
    assert not deep_equal([4, 5], [4, 5, 6])

def test_objects():
    assert deep_equal({'b': 2, 'a': 1}, {'a': 1, 'b': 2})
    assert not deep_equal({'a': 1, 'b': 3}, {'a': 1, 'b': 2})
    assert not deep_equal({'a': 1}, {'a': 1, 'b': 2})

def test_nested_objects_and_arrays():
    a = {'c': [4, {'d': 5}], 'e': {'f': 7}}
    b = {'c': [4, {'d': 5}], 'e': {'f': 7}}
    c = {'c': [4, {'d': 8}], 'e': {'f': 7}}
    assert deep_equal(a, b)
    assert not deep_equal(a, c)