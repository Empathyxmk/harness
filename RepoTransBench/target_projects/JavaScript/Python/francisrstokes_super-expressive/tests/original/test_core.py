import pytest
import types
from src.super_expressive import core

# Attempt to get all exports from core module
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

# --- assert
def test_assert_does_not_throw_on_truthy():
    assert_(True, "should not throw")
    assert_(1)

def test_assert_throws_on_falsy():
    with pytest.raises(Exception) as e:
        assert_(False, "error msg")
    assert str(e.value) == "error msg"
    with pytest.raises(Exception) as e:
        assert_(0, "fail")
    assert str(e.value) == "fail"

# --- asType
def test_asType_returns_function_that_wraps_value_with_type():
    t = asType('num')
    assert t(5) == {'type': 'num', 'value': 5}
    t2 = asType('foo', {'a': 1})
    assert t2('bar') == {'type': 'foo', 'value': 'bar', 'a': 1}
    t3 = asType('custom', {'test': True})
    assert callable(t3)
    assert t3(None) == {'type': 'custom', 'value': None, 'test': True}

# --- deferredType
def test_deferredType_returns_type_with_itself_as_value():
    dt = deferredType('foo', {'b':2})
    assert callable(dt['value'])
    assert dt['type'] == 'foo'
    assert dt['b'] == 2

# --- deepCopy
def test_deepCopy_primitives():
    assert deepCopy(5) == 5
    assert deepCopy('abc') == 'abc'
    assert deepCopy(None) is None
    assert deepCopy(core.UNDEFINED) is core.UNDEFINED if hasattr(core, "UNDEFINED") else True

def test_deepCopy_arrays():
    arr = [1, [2], {'a':3}]
    copy = deepCopy(arr)
    assert copy == arr
    assert copy is not arr
    assert copy[1] is not arr[1]
    assert copy[2] is not arr[2]

def test_deepCopy_object():
    obj = {'x':1, 'y':{'z':2}}
    copy = deepCopy(obj)
    assert copy == obj
    assert copy is not obj
    assert copy['y'] is not obj['y']

def test_deepCopy_does_not_clone_date_or_regex():
    import datetime, re
    dt = datetime.datetime.now()
    assert deepCopy(dt) is dt
    rx = re.compile('abc')
    assert deepCopy(rx) is rx

# --- partition
def test_partition_partitions_an_array():
    arr = [1,2,3,4]
    evens, odds = partition(lambda x: x%2 == 0, arr)
    assert evens == [2,4]
    assert odds == [1,3]

def test_partition_empty_input():
    a, b = partition(lambda _: True, [])
    assert a == []
    assert b == []

def test_partition_all_to_left_or_right():
    left, right = partition(lambda _: True, [1,2])
    assert left == [1,2]
    assert right == []
    left2, right2 = partition(lambda _: False, [1,2])
    assert left2 == []
    assert right2 == [1,2]

# --- replaceAll
def test_replaceAll_replaces_all():
    assert replaceAll("abcabc", "a", "x") == 'xbcxbc'
    assert replaceAll("aa$bb$", "$", "#") == "aa#bb#"
    assert replaceAll("hello.", ".", "!") == "hello!"

def test_replaceAll_handles_special_chars_and_no_match():
    assert replaceAll("abcdef", "$", "#") == "abcdef"
    assert replaceAll("foo-bar-foo", "-", "@") == "foo@bar@foo"

# --- escapeSpecial
def test_escapeSpecial_escapes_special_chars():
    assert escapeSpecial("1+1=2?") == "1\\+1=2\\?"
    assert escapeSpecial(".[]") == '\\.\\[\\]'
    assert escapeSpecial("a$b^c") == 'a\\$b\\^c'

def test_escapeSpecial_no_special_chars():
    assert escapeSpecial("abc") == "abc"

def test_escapeSpecial_mix_of_escaped_and_not():
    assert escapeSpecial("[a-z]") == "\\[a\\-z\\]"

# --- applySubexpressionDefaults
def test_applySubexpressionDefaults_applies_defaults_and_allows_overrides():
    input_obj = {'foo':1, 'namespace':"bob", 'ignoreStartAndEnd':False}
    out = applySubexpressionDefaults(input_obj)
    assert out['namespace'] == "bob"
    assert out['ignoreFlags'] == True
    assert out['ignoreStartAndEnd'] == False
    assert out['foo'] == 1

def test_applySubexpressionDefaults_sets_bare_defaults():
    out = applySubexpressionDefaults({})
    assert out['namespace'] == ""
    assert out['ignoreFlags'] == True
    assert out['ignoreStartAndEnd'] == True

def test_applySubexpressionDefaults_throws_on_invalid_types():
    with pytest.raises(Exception):
        applySubexpressionDefaults({'namespace': 5})
    with pytest.raises(Exception):
        applySubexpressionDefaults({'ignoreFlags':'y'})
    with pytest.raises(Exception):
        applySubexpressionDefaults({'ignoreStartAndEnd':None})

# --- quantifierTable
def test_quantifierTable_functions():
    q = quantifierTable
    assert q['oneOrMore'] == '+'
    assert q['oneOrMoreLazy'] == '+?'
    assert q['zeroOrMore'] == '*'
    assert q['zeroOrMoreLazy'] == '*?'
    assert q['optional'] == '?'
    assert q['exactly'](5) == '{5}'
    assert q['atLeast'](2) == '{2,}'
    assert q['atLeastLazy'](3) == '{3,}?'
    assert q['between']([1,4]) == '{1,4}'
    assert q['betweenLazy']([2,5]) == '{2,5}?'

# --- regexes
def test_namedGroupRegex():
    rg = namedGroupRegex
    assert rg.match('group')
    assert not rg.match('_bad')
    assert rg.match('a1')
    assert rg.match('Bxy_z')
    assert not rg.match('6foo')

def test_singleUnicodeCharRegex():
    rg = singleUnicodeCharRegex
    assert rg.match('a')
    assert not rg.match('')
    assert not rg.match('xx')
    assert rg.match('🤖')

def test_controlCharRegex():
    rg = controlCharRegex
    assert rg.match('a')
    assert rg.match('Z')
    assert not rg.match('!')
    assert not rg.match('aa')

def test_hexadecimalStringRegex():
    rg = hexadecimalStringRegex
    assert rg.match('1aFF')
    assert rg.match('deadbeef')
    assert not rg.match('xyz')
    assert not rg.match('')