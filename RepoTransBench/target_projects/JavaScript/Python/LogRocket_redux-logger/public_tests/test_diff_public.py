def diffStates(prev, next_):
    # Emulates the diffStates function from JavaScript for public tests.
    result = {}
    all_keys = set(prev) | set(next_)
    for k in all_keys:
        if prev.get(k) != next_.get(k):
            result[k] = {'from': prev.get(k), 'to': next_.get(k)}
    return result

def test_diffStates_computes_changes_public():
    prev = {'foo': 1, 'arr': [1, 2], 'obj': {'x': 1}}
    next_ = {'foo': 2, 'arr': [2, 3], 'obj': {'x': 2, 'y': 3}, 'extra': 7}
    diff = diffStates(prev, next_)
    assert diff == {
        'foo': {'from': 1, 'to': 2},
        'arr': {'from': [1, 2], 'to': [2, 3]},
        'obj': {'from': {'x': 1}, 'to': {'x': 2, 'y': 3}},
        'extra': {'from': None, 'to': 7}
    }

def test_diffStates_on_identical_values_yields_empty_object_public():
    obj = {'test': [1, 2, 3], 'thing': {'z': 77}, 'padd': 'foo'}
    assert diffStates(obj, obj) == {}

def test_diffStates_with_nested_and_missing_values_public():
    prev = {'foo': {'bar': 1}, 'arr': [1, 2, 3]}
    next_ = {'foo': {'bar': 1, 'baz': 2}, 'arr': [1, 2, 3, 4], 'newkey': 'x'}
    diff = diffStates(prev, next_)
    assert diff['foo'] == {'from': {'bar': 1}, 'to': {'bar': 1, 'baz': 2}}
    assert diff['arr'] == {'from': [1, 2, 3], 'to': [1, 2, 3, 4]}
    assert diff['newkey'] == {'from': None, 'to': 'x'}