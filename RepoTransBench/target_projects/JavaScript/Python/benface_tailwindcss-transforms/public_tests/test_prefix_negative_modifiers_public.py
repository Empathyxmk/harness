from benface_tailwindcss_transforms.prefix_negative_modifiers import prefix_negative_modifiers

def test_is_defined_if_exported_public():
    assert callable(prefix_negative_modifiers)

def test_returns_object_unchanged_when_values_are_arrays_objects():
    out = prefix_negative_modifiers({'foo': [42], 'bar': {'a': 1}})
    assert out == {'foo': [42], 'bar': {'a': 1}}

def test_adds_prefix_to_different_negative_number_values():
    out = prefix_negative_modifiers({'x': -10, 'y': 3})
    assert out == {'x': "-10", 'y': "3"}

def test_adds_prefix_to_other_negative_string_numbers():
    out = prefix_negative_modifiers({'x': "-7", 'y': "9"})
    assert out == {'x': "-7", 'y': "9"}

def test_handles_another_empty_object():
    assert prefix_negative_modifiers({}) == {}

def test_handles_zero_negative_zero_and_string_negative_zero():
    out = prefix_negative_modifiers({'x': 0, 'y': "-0", 'z': -0})
    assert out == {'x': "0", 'y': "-0", 'z': "0"}