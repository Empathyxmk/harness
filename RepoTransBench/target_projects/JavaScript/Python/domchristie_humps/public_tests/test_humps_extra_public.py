import pytest
import re
from src.humps import (
    camelize,
    pascalize,
    decamelize,
    camelizeKeys,
    decamelizeKeys,
    pascalizeKeys,
    depascalizeKeys
)

def undefined_equivalent_public():
    """A sentinel for JS-like undefined (since Python's None is used for null)."""
    class _Undef: pass
    if not hasattr(undefined_equivalent_public, '_val'):
        undefined_equivalent_public._val = _Undef()
    return undefined_equivalent_public._val

def make_date_public(year, month, day):
    import datetime
    # JS months are 0-based, so (2020,1,2) means Feb 2, 2020 in JS.
    # We'll mimic 1-based for easier Python code, since all test logic is in Python now.
    return datetime.datetime(year, month, day)

def test_camelize_handles_multiple_delimiters_public():
    assert camelize("bar_foo-baz quux") == "barFooBazQuux"

def test_camelize_numerical_strings_public():
    assert camelize("456") == "456"

def test_camelize_lowercases_first_character_public():
    assert camelize("TEST_CASE") == "tESTCASE"

def test_camelize_empty_string_public():
    assert camelize("") == ""

def test_pascalize_capitalizes_first_letter_public():
    assert pascalize("bar_foo") == "BarFoo"

def test_pascalize_handles_camel_case_public():
    assert pascalize("barFooBaz") == "BarFooBaz"

def test_pascalize_empty_string_public():
    assert pascalize("") == ""

def test_decamelize_camelcase_to_snake_case_public():
    assert decamelize("barFooBaz") == "bar_foo_baz"

def test_decamelize_custom_separator_public():
    assert decamelize("barFooBaz", "-") == "barfoobaz"

def test_decamelize_no_change_on_snake_case_public():
    assert decamelize("bar_foo_baz") == "bar_foo_baz"

def test_decamelizekeys_non_object_values_public():
    assert decamelizeKeys(5678) == 5678
    assert decamelizeKeys(None) is None
    assert decamelizeKeys(undefined_equivalent_public()) is undefined_equivalent_public()
    assert decamelizeKeys(False) is False
    assert decamelizeKeys(True) is True

    d = make_date_public(2020, 2, 2)
    assert decamelizeKeys(d) is d

    r = re.compile('def')
    assert decamelizeKeys(r) is r

def test_decamelizekeys_dates_unchanged_except_key_public():
    d = make_date_public(2030, 6, 1)
    obj = {'someDate': d}
    result = decamelizeKeys(obj)
    assert 'some_date' in result and result['some_date'] is d

def test_decamelizekeys_regexp_boolean_keys_public():
    r = re.compile('b')
    bool_val = False
    obj = {'regExPattern': r, 'boolFlag': bool_val}
    result = decamelizeKeys(obj)
    assert 'reg_ex_pattern' in result and result['reg_ex_pattern'] is r
    assert 'bool_flag' in result and result['bool_flag'] is bool_val

def test_camelizeKeys_proto_vs_own_property_public():
    class Bar:
        def protoMeth(self): return 4
    Bar.protoAttr = 5
    b = Bar()
    def ownMeth(): return 5
    b.ownMeth = ownMeth
    hk = camelizeKeys(b)
    assert 'ownMeth' in hk
    assert 'protoMeth' not in hk

def test_camelizeKeys_arrays_public():
    arr = [{'bar_foo': 3}, {'bar_baz': 4}]
    expected = [{'barFoo': 3}, {'barBaz': 4}]
    assert camelizeKeys(arr) == expected

def test_pascalizeKeys_recursively_public():
    o = {'alpha_beta': {'gamma_delta': 7}}
    r = pascalizeKeys(o)
    assert 'AlphaBeta' in r and 'GammaDelta' in r['AlphaBeta']

def test_decamelizeKeys_object_keys_public():
    o = {'alphaBeta': {'gammaDelta': 7}}
    r = decamelizeKeys(o)
    assert 'alpha_beta' in r and 'gamma_delta' in r['alpha_beta']

def test_depascalizeKeys_public():
    o = {'AlphaBeta': {'GammaDelta': 7}}
    r = depascalizeKeys(o)
    assert 'alpha_beta' in r and 'gamma_delta' in r['alpha_beta']

def test_decamelizeKeys_custom_separator_public():
    o = {'coolKey': 9, 'hotKey': 10}
    r = decamelizeKeys(o, {'separator': '.'})
    assert 'cool.key' in r and 'hot.key' in r

def test_pascalizeKeys_arrays_public():
    arr = [{'alpha_beta': 123}]
    r = pascalizeKeys(arr)
    assert isinstance(r, list)
    assert 'AlphaBeta' in r[0]

def test_custom_process_callback_in_options_public():
    obj = {'alpha_beta': 88, 'gamma_delta': 77}
    opt = {'process': lambda k, *_: 'x_' + k, 'recursive': True}
    r = camelizeKeys(obj, opt)
    assert 'x_alpha_beta' in r and 'x_gamma_delta' in r

def test_process_callback_not_a_function_fallback_public():
    obj = {'alpha_beta': 44}
    opt = {'process': 0, 'recursive': True}
    r = camelizeKeys(obj, opt)
    assert 'alphaBeta' in r

def test_humps_module_exports_public():
    import src.humps as humps
    assert hasattr(humps, 'camelize')
    assert hasattr(humps, 'decamelize')
    assert hasattr(humps, 'pascalize')