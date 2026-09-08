import pytest
import re
from src.humps import (
    camelize,
    pascalize,
    decamelize,
    camelizeKeys,
    decamelizeKeys,
    pascalizeKeys,
    depascalizeKeys,
)

def undefined_equivalent():
    """A sentinel for JS-like undefined (since Python's None is used for null)."""
    # Singleton for undefined
    class _Undef: pass
    if not hasattr(undefined_equivalent, '_val'):
        undefined_equivalent._val = _Undef()
    return undefined_equivalent._val

def make_date():
    import datetime
    return datetime.datetime.now()  # For dynamic date object testing

def test_camelize_handles_multiple_delimiters():
    assert camelize('foo-bar_baz qux') == 'fooBarBazQux'

def test_camelize_numerical_strings():
    assert camelize('123') == '123'

def test_camelize_lowercases_first_character():
    assert camelize('HELLO_WORLD') == 'hELLOWORLD'

def test_camelize_empty_string():
    assert camelize('') == ''

def test_pascalize_capitalizes_first_letter():
    assert pascalize('foo_bar') == 'FooBar'

def test_pascalize_handles_camel_case():
    assert pascalize('fooBarBaz') == 'FooBarBaz'

def test_pascalize_empty_string():
    assert pascalize('') == ''

def test_decamelize_camelcase_to_snake_case():
    assert decamelize('fooBarBaz') == 'foo_bar_baz'

def test_decamelize_custom_separator():
    # As per sourcenote, actual behavior may be to return 'foobarbaz'
    result = decamelize('fooBarBaz', '-')
    assert result == 'foobarbaz'

def test_decamelize_no_change_on_snake_case():
    assert decamelize('foo_bar_baz') == 'foo_bar_baz'

def test_decamelizekeys_non_object_values():
    # js: humps.decamelizeKeys(undefined) -- Python can't have an 'undefined', so use the sentinel
    assert decamelizeKeys(1234) == 1234
    assert decamelizeKeys(None) is None
    assert decamelizeKeys(undefined_equivalent()) is undefined_equivalent()
    assert decamelizeKeys(True) is True
    assert decamelizeKeys(False) is False

    d = make_date()
    assert decamelizeKeys(d) is d

    r = re.compile('abc')
    assert decamelizeKeys(r) is r

def test_decamelizekeys_dates_unchanged_except_key():
    d = make_date()
    obj = {'dateValue': d}
    result = decamelizeKeys(obj)
    assert 'date_value' in result and result['date_value'] is d

def test_decamelizekeys_regexp_boolean_keys():
    r = re.compile('a')
    bool_val = True
    obj = {'regExpValue': r, 'boolValue': bool_val}
    result = decamelizeKeys(obj)
    assert 'reg_exp_value' in result and result['reg_exp_value'] is r
    assert 'bool_value' in result and result['bool_value'] is bool_val

def test_camelizeKeys_proto_vs_own_property():
    class Foo:
        def protoFunc(self): return 1
    Foo.protoVar = 2
    f = Foo()
    def ownFunc(): return 2
    f.ownFunc = ownFunc
    hk = camelizeKeys(f)
    assert 'ownFunc' in hk
    assert 'protoFunc' not in hk

def test_camelizeKeys_arrays():
    input_arr = [{'foo_bar': 1}, {'foo_baz': 2}]
    expect_arr = [{'fooBar': 1}, {'fooBaz': 2}]
    assert camelizeKeys(input_arr) == expect_arr

def test_pascalizeKeys_recursively():
    o = {'foo_bar': {'baz_qux': 1}}
    r = pascalizeKeys(o)
    assert 'FooBar' in r and 'BazQux' in r['FooBar']

def test_decamelizeKeys_object_keys():
    o = {'fooBar': {'bazQux': 1}}
    r = decamelizeKeys(o)
    assert 'foo_bar' in r and 'baz_qux' in r['foo_bar']

def test_depascalizeKeys():
    o = {'FooBar': {'BazQux': 1}}
    r = depascalizeKeys(o)
    assert 'foo_bar' in r and 'baz_qux' in r['foo_bar']

def test_decamelizeKeys_custom_separator():
    o = {'someKey': 1, 'otherKey': 2}
    r = decamelizeKeys(o, {'separator': '-'})
    assert 'some-key' in r and 'other-key' in r

def test_pascalizeKeys_arrays():
    arr = [{'foo_bar': 1}]
    r = pascalizeKeys(arr)
    assert isinstance(r, list)
    assert 'FooBar' in r[0]

def test_custom_process_callback_in_options():
    obj = {'foo_bar': 1, 'baz_qux': 2}
    opt = {'process': lambda k, *_: 'prefix_' + k, 'recursive': True}
    r = camelizeKeys(obj, opt)
    assert 'prefix_foo_bar' in r
    assert 'prefix_baz_qux' in r

def test_process_callback_not_a_function_fallback():
    obj = {'foo_bar': 1}
    opt = {'process': True, 'recursive': True}
    r = camelizeKeys(obj, opt)
    assert 'fooBar' in r

def test_humps_module_exports():
    import src.humps as humps
    assert hasattr(humps, 'camelize')
    assert hasattr(humps, 'decamelize')
    assert hasattr(humps, 'pascalize')