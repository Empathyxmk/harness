def test_delete_operator_on_object_property_public():
    obj = {'alpha': 123, 'beta': 456}
    assert 'alpha' in obj
    obj.pop('alpha', None)
    assert obj.get('alpha') is None
    assert 'beta' in obj

def test_delete_operator_on_array_element_public():
    arr = [10, 20, 30]
    arr[1] = None  # Python's 'del arr[1]' would change length, simulating JS 'delete' sets to undefined
    assert arr[1] is None
    assert len(arr) == 3