import pytest
import types
from src.get_value import get_value

def test_should_get_a_direct_property():
    obj = {'a': 1}
    assert get_value(obj, 'a') == 1

def test_should_return_default_value_if_property_does_not_exist():
    obj = {}
    assert get_value(obj, 'foo', {'default': 'bar'}) == 'bar'

def test_should_handle_nested_properties_with_dot_notation():
    obj = {'foo': {'bar': {'baz': 'qux'}}}
    assert get_value(obj, 'foo.bar.baz') == 'qux'

def test_should_handle_array_path():
    obj = {'foo': {'bar': 'baz'}}
    assert get_value(obj, ['foo', 'bar']) == 'baz'

def test_should_handle_numeric_path():
    obj = {'1': 'one'}
    assert get_value(obj, 1) == 'one'

def test_should_return_default_when_accessing_property_on_non_object():
    assert get_value(None, 'foo', {'default': 123}) == 123
    assert get_value(None, 'foo', {'default': 123}) == 123

def test_should_return_original_value_if_path_is_not_string_array():
    obj = {'foo': 'bar'}
    assert get_value(obj, {}) == obj

def test_should_use_a_custom_split_function():
    obj = {'foo': {'bar': 'baz'}}
    options = {
        'split': lambda path: path.split('#')
    }
    assert get_value(obj, 'foo#bar', options) == 'baz'

def test_should_use_a_custom_join_function():
    obj = {'foo#bar': 'baz'}
    options = {
        'join': lambda segs: '#'.join(segs),
        'separator': '#'
    }
    assert get_value(obj, 'foo#bar', options) == 'baz'

def test_should_use_custom_is_valid_to_filter_properties():
    obj = {'foo': 'bar', 'bar': 'baz'}
    options = {
        'isValid': lambda key: key == 'foo'
    }
    assert get_value(obj, 'foo', options) == 'bar'
    assert get_value(obj, 'bar', options) is None

def test_should_support_path_segments_with_escaped_separator():
    obj = {'foo.bar': {'baz': 'buzz'}}
    assert get_value(obj, r'foo\.bar.baz') == 'buzz'

def test_should_properly_handle_multi_segment_join_with_joinChar():
    obj = {'foo|bar|baz': 'abc'}
    options = {
        'separator': '|',
        'joinChar': '|'
    }
    assert get_value(obj, 'foo|bar|baz', options) == 'abc'

def test_should_properly_handle_property_that_is_a_function():
    def func():
        return 42
    obj = {'foo': func}
    result = get_value(obj, 'foo')
    assert callable(result)
    assert result() == 42

def test_should_support_options_being_a_primitive_and_treat_as_default():
    obj = {}
    assert get_value(obj, 'foo', 'DEFAULT') == 'DEFAULT'

def test_should_handle_empty_path_string():
    obj = {'': 42}
    assert get_value(obj, '', {}) == 42

def test_should_return_default_when_target_is_not_an_object_or_function():
    assert get_value(123, 'a', {'default': 'D'}) == 'D'
    assert get_value(None, 'a') is None