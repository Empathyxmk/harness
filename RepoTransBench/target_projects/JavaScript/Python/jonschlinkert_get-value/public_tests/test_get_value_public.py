import pytest
from src.get_value import get_value

# 1. Basic property access, different keys and values
def test_public_should_get_property_from_top_level_object():
    assert get_value({'engine': 'v8'}, 'engine') == 'v8'

def test_public_should_return_undefined_for_non_existent_property():
    assert get_value({'foo': 123}, 'bar') is None

# 2. Nested property access with string path, new structure
def test_public_should_get_deeply_nested_property():
    obj = {'a': {'b': {'c': 'deepValue'}}}
    assert get_value(obj, 'a.b.c') == 'deepValue'

def test_public_should_return_default_value_if_property_does_not_exist():
    obj = {'x': {'y': {'z': 0}}}
    assert get_value(obj, 'x.y.w', {'default': 'notfound'}) == 'notfound'

# 3. Nested property access with array path, different nesting
def test_public_should_get_nested_property_via_array_path():
    obj = {'john': {'profile': {'age': 42}}}
    assert get_value(obj, ['john', 'profile', 'age']) == 42

def test_public_should_return_default_for_wrong_path_with_array():
    obj = {'one': {'two': 2}}
    assert get_value(obj, ['one', 'three'], {'default': 99}) == 99

# 4. Numeric paths (array index) and number coercion, with different data
def test_public_should_access_array_index_property():
    arr = ['zero', 'uno', 'dos']
    assert get_value(arr, 2) == 'dos'

def test_public_should_return_default_for_missing_array_index():
    arr = [5, 4, 3]
    assert get_value(arr, 10, {'default': 'empty'}) == 'empty'

# 5. Option: custom separator and joinChar
def test_public_should_use_custom_separator():
    obj = {'foo/bar': {'baz': 'zzz'}}
    # separator is '.' but there's no '.', so normal path splitting (should find 'foo/bar') then 'baz'
    assert get_value(obj, 'foo/bar.baz', {'separator': '.'}) == 'zzz'

def test_public_should_use_custom_separator_other_char():
    obj = {'p|q': {'r': 12}}
    assert get_value(obj, 'p|q|r', {'separator': '|'}) == 12

# 6. Escaped separator property name (with \)
def test_public_should_get_property_with_literal_dot_in_name():
    obj = {'main.sub': {'x': 'val'}}
    assert get_value(obj, r'main\.sub.x') == 'val'

def test_public_should_get_property_with_double_backslash_escape():
    obj = {'level1\\level2': {'leaf': 'leafy'}}
    assert get_value(obj, r'level1\\level2.leaf', {'separator': '.'}) == 'leafy'

# 7. isValid and split/join function options (custom scenario)
def test_public_should_use_custom_isvalid_to_deny_property():
    obj = {'block': {'safe': 'yes'}}
    options = {'isValid': lambda key, target=None: key != 'block'}
    assert get_value(obj, 'block.safe', options) is None

def test_public_should_use_custom_split_and_join_functions_for_paths():
    obj = {'a___b': {'c': 101}}
    options = {
        'split': lambda p: p.split('***'),
        'join': lambda segs: '___'.join(segs)
    }
    assert get_value(obj, 'a***b.c', options) == 101

# 8. Non-object targets and default value behavior
def test_public_should_return_default_for_null_input():
    assert get_value(None, 'abc', {'default': 'fallback'}) == 'fallback'

def test_public_should_return_primitive_target_if_no_valid_object():
    assert get_value('primitive', 'anything') == 'primitive'

# 9. Function as object target (should behave as object)
def test_public_should_get_property_of_a_function_target():
    def foo():
        pass
    foo.bar = 'bazfunc'
    assert get_value(foo, 'bar') == 'bazfunc'

# 10. Path is array, property name as number key string
def test_public_should_return_value_for_number_key_as_string():
    obj = {'12': 'dozen'}
    assert get_value(obj, ['12']) == 'dozen'