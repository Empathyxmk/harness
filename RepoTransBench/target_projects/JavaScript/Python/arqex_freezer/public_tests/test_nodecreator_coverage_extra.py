from src import nodeCreator

def test_return_value_for_null_undefined_boolean_public():
    assert nodeCreator.createNode(None) is None
    assert nodeCreator.createNode(None) is None
    assert nodeCreator.createNode(True) is True

def test_create_frozen_array_object_with_deep_data_public():
    obj = nodeCreator.createNode({'arr': [{'deep': 5}]})
    assert getattr(obj, '_is_frozen', False) is True or hasattr(obj, '_frozen')
    assert getattr(obj['arr'], '_is_frozen', False) is True or hasattr(obj['arr'], '_frozen')
    assert getattr(obj['arr'][0], '_is_frozen', False) is True or hasattr(obj['arr'][0], '_frozen')
    assert obj['arr'][0]['deep'] == 5