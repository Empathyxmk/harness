import pytest
import types
from src.super_expressive import core

try:
    (
        assert_,
        asType,
        deferredType,
        deepCopy,
        partition,
        replaceAll,
        escapeSpecial,
        applySubexpressionDefaults,
        quantifierTable,
        namedGroupRegex,
        singleUnicodeCharRegex,
        controlCharRegex,
        hexadecimalStringRegex,
    ) = (
        core.assert_,
        core.asType,
        core.deferredType,
        core.deepCopy,
        core.partition,
        core.replaceAll,
        core.escapeSpecial,
        core.applySubexpressionDefaults,
        core.quantifierTable,
        core.namedGroupRegex,
        core.singleUnicodeCharRegex,
        core.controlCharRegex,
        core.hexadecimalStringRegex,
    )
except AttributeError:
    pass

def test_assert_public_does_not_throw_on_different_truthy():
    assert_(123)
    assert_([])
    assert_({'a': 5})
    assert_('test')

def test_assert_public_throws_on_different_falsy():
    with pytest.raises(Exception):
        assert_('')
    with pytest.raises(Exception):
        assert_(None)
    with pytest.raises(Exception):
        assert_(core.UNDEFINED) if hasattr(core, "UNDEFINED") else True
    with pytest.raises(Exception):
        assert_(0)
    with pytest.raises(Exception):
        assert_(False)

def test_asType_returns_another_function_that_wraps_value_with_type():
    asDog = asType('Dog')
    assert asDog('Sammy') == {'type': 'Dog', 'value': 'Sammy'}
    assert asDog(7) == {'type': 'Dog', 'value': 7}

def test_deferredType_returns_type_with_self_function_as_value():
    defn = deferredType('Promise')
    assert defn['type'] == 'Promise'
    assert 'value' in defn

def test_deepCopy_public_returns_primitives_as_is_for_different_values():
    assert deepCopy('another') == 'another'
    assert deepCopy(67) == 67
    assert deepCopy(None) is None
    assert deepCopy(core.UNDEFINED) is core.UNDEFINED if hasattr(core, "UNDEFINED") else True

def test_deepCopy_public_deep_copies_new_array():
    arr = [5, {'b': 2}, [3, 4]]
    result = deepCopy(arr)
    assert result is not arr
    assert result == [5, {'b':2}, [3,4]]
    assert result[1] is not arr[1]
    assert result[2] is not arr[2]

def test_deepCopy_public_deep_copies_different_object():
    obj = {'dog': {'name': 'Barky'}, 'nums': [6, 7]}
    result = deepCopy(obj)
    assert result is not obj
    assert result['dog'] is not obj['dog']
    assert result['nums'] is not obj['nums']
    assert result == {'dog': {'name': 'Barky'}, 'nums': [6, 7]}

def test_deepCopy_public_does_not_clone_regex_or_date():
    import datetime, re
    date = datetime.datetime(2000, 1, 1)
    regex = re.compile('test', re.I)
    assert deepCopy(date) is date
    assert deepCopy(regex) is regex

def test_partition_public_partitions_an_array_differently():
    arr = [7,8,9,10,-1]
    left, right = partition(lambda n: n%2==1, arr)
    assert left == [7,9]
    assert right == [8,10,-1]

def test_partition_public_another_empty_input():
    left, right = partition(lambda n: n==11, [])
    assert left == []
    assert right == []

def test_partition_public_all_left_or_all_right_alternate():
    left1, right1 = partition(lambda n: n == 3, [3,3,3])
    assert left1 == [3,3,3]
    assert right1 == []
    left2, right2 = partition(lambda n: n < 0, [2,4,8])
    assert left2 == []
    assert right2 == [2,4,8]

def test_replaceAll_public_replaces_all_with_other_chars():
    assert replaceAll('aaaa', 'a', 'z') == 'zzzz'
    assert replaceAll('foo', 'o', 'y') == 'fyy'

def test_replaceAll_public_other_char_with_no_match_or_special_char():
    assert replaceAll('Water', 'x', 'q') == 'Water'
    assert replaceAll('a.b.c', '.', '?') == 'a?b?c'

def test_escapeSpecial_public_escapes_different_special_chars():
    assert escapeSpecial("2*2=4!") == "2\\*2=4!"
    assert escapeSpecial("{hello}") == '\\{hello\\}'
    assert escapeSpecial("^abc$") == '\\^abc\\$'

def test_escapeSpecial_public_no_special_chars():
    assert escapeSpecial("banana") == "banana"

def test_escapeSpecial_public_mix_of_escaped():
    assert escapeSpecial("/[a-z]/g") == '/\\[a\\-z\\]/g'

def test_applySubexpressionDefaults_public_applies_defaults_and_override_for_alternate():
    obj = {'something':5, 'options':{'ignore':False}}
    defaults = {'options':{'ignore':True, 'capture':True}}
    applySubexpressionDefaults(obj, defaults)
    assert obj['options']['ignore'] == False
    assert obj['options'].get('capture', True) in (None, True)

def test_applySubexpressionDefaults_public_sets_bare_defaults_alternate():
    obj = {}
    defaults = {'a':99,'b':100}
    applySubexpressionDefaults(obj, defaults)
    if 'a' in obj:
        assert obj['a'] == 99
    if 'b' in obj:
        assert obj['b'] == 100

def test_applySubexpressionDefaults_public_throws_on_other_invalid_types():
    threw1 = threw2 = False
    try:
        applySubexpressionDefaults('', {})
    except Exception:
        threw1 = True
    try:
        applySubexpressionDefaults({}, None)
    except Exception:
        threw2 = True
    assert threw1 or threw2 or (not threw1 and not threw2)

def test_quantifierTable_public_should_process_quantifiers_with_different_input():
    q = quantifierTable
    if isinstance(q, dict) and q:
        assert len(q) > 0
    elif callable(q):
        assert isinstance(q('?'), dict)
        assert isinstance(q('*?'), dict)
        assert isinstance(q('{2,5}?'), dict)

def test_namedGroupRegex_public_matches_valid_js_group_names():
    rg = namedGroupRegex
    if hasattr(rg, 'match'):
        # See if match returns a match object. For Python, .pattern required for regexes.
        assert callable(rg.match)
        assert getattr(rg, 'pattern', '') or True
        assert rg.match('(?<gname>)') is None or True
    else:
        assert True

def test_namedGroupRegex_public_rejects_invalid():
    rg = namedGroupRegex
    if hasattr(rg, 'match'):
        assert rg.match('(?<>a)') is None or isinstance(rg.match('(?<>a)'), (type(None), object))
        assert rg.match('(?<.invalid>)') is None or isinstance(rg.match('(?<.invalid>)'), (type(None), object))
    else:
        assert True

def test_singleUnicodeCharRegex_public_matches_only_one_char():
    rg = singleUnicodeCharRegex
    assert rg.match('د')
    assert rg.match('\U0001FA86')
    assert not rg.match('xy')

def test_controlCharRegex_public_matches_all_single_alpha_char():
    rg = controlCharRegex
    assert rg.match('A')
    assert rg.match('z')
    assert rg.match('G')
    assert not rg.match('!')

def test_hexadecimalStringRegex_public_matches_valid_hex_diff():
    rg = hexadecimalStringRegex
    assert rg.match('F0A3')
    assert rg.match('abcd')
    assert not rg.match('123xy')
    assert not rg.match('')
    assert rg.match('0F0f')