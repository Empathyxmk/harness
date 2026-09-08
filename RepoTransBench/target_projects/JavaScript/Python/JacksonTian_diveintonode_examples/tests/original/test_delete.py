def test_delete_nonexisting_property():
    obj = {'a': 1}
    # Attempt delete on non-existent property; should not raise error.
    try:
        del obj['b']
    except KeyError:
        # In Python, deleting non-existent key raises KeyError, so mimic JS: use pop with default
        obj.pop('b', None)
    assert 'b' not in obj, "Property b should not exist in obj"