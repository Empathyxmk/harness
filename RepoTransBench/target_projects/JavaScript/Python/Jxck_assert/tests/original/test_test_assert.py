import pytest
import types
from src.jxck_assert import *

def make_block(f, *args, **kwargs):
    def block():
        return f(*args, **kwargs)
    return block

def test_basics():
    throws(make_block(ok, False), AssertionError)
    doesNotThrow(make_block(ok, True), AssertionError)
    doesNotThrow(make_block(ok, 'test'), AssertionError)
    throws(make_block(ok, False), AssertionError)
    doesNotThrow(make_block(ok, True), AssertionError)
    doesNotThrow(make_block(ok, 'test'))
    throws(make_block(equal, True, False), AssertionError)
    doesNotThrow(make_block(equal, None, None))
    doesNotThrow(make_block(equal, None, None))
    doesNotThrow(make_block(equal, None, None))
    doesNotThrow(make_block(equal, True, True))
    doesNotThrow(make_block(equal, 2, '2'))
    doesNotThrow(make_block(notEqual, True, False))
    throws(make_block(notEqual, True, True), AssertionError)
    throws(make_block(strictEqual, 2, '2'), AssertionError)
    throws(make_block(strictEqual, None, None), AssertionError)
    doesNotThrow(make_block(notStrictEqual, 2, '2'))

def test_deep_equals_joy():
    # 7.2
    import datetime
    date1 = datetime.datetime(2000, 4, 14)
    date2 = datetime.datetime(2000, 4, 14)
    doesNotThrow(make_block(deepEqual, date1, date2))
    doesNotThrow(make_block(deepEqual, date1, date2))
    with pytest.raises(Exception):
        deepEqual(datetime.datetime.now(), date2)

    # 7.3 RegExp => in python, use re pattern objects
    import re
    pattern1 = re.compile('a')
    pattern2 = re.compile('a')
    doesNotThrow(make_block(deepEqual, pattern1, pattern2))
    # Unlike JS, but for demonstration.
    doesNotThrow(make_block(deepEqual, pattern1, pattern2))
    with pytest.raises(Exception):
        deepEqual(re.compile('ab'), re.compile('a'))

    doesNotThrow(make_block(deepEqual, 4, '4'))
    doesNotThrow(make_block(deepEqual, True, 1))
    with pytest.raises(Exception):
        deepEqual(4, '5')

    doesNotThrow(make_block(deepEqual, {'a': 4}, {'a': 4}))
    doesNotThrow(make_block(deepEqual, {'a': 4, 'b': '2'}, {'a': 4, 'b': '2'}))
    doesNotThrow(make_block(deepEqual, [4], ['4']))
    with pytest.raises(Exception):
        deepEqual({'a': 4}, {'a': 4, 'b': True})
    doesNotThrow(make_block(deepEqual, ['a'], {'0': 'a'}))
    doesNotThrow(make_block(deepEqual, {'a': 4, 'b': '1'}, {'b': '1', 'a': 4}))
    a1 = [1, 2, 3]
    a2 = [1, 2, 3]
    # Add attributes
    a1_obj = types.SimpleNamespace(**{'a': 'test', 'b': True})
    a2_obj = types.SimpleNamespace(**{'b': True, 'a': 'test'})
    a1_attrs = list(a1_obj.__dict__.keys())
    a2_attrs = list(a2_obj.__dict__.keys())
    # These are different kinds of dict keys.
    with pytest.raises(Exception):
        deepEqual(a1_attrs, a2_attrs)

def test_deep_equal_with_prototypes():
    class NbRoot:
        def __str__(self):
            return self.first + ' ' + self.last

    class NameBuilder(NbRoot):
        def __init__(self, first, last):
            self.first = first
            self.last = last
    
    class NameBuilder2(NbRoot):
        def __init__(self, first, last):
            self.first = first
            self.last = last

    nb1 = NameBuilder('Ryan', 'Dahl')
    nb2 = NameBuilder2('Ryan', 'Dahl')

    doesNotThrow(make_block(deepEqual, nb1, nb2))
    # Now, change the "prototype" to a plain object
    class NameBuilder2_Other:
        def __init__(self, first, last):
            self.first = first
            self.last = last

    nb2 = NameBuilder2_Other('Ryan', 'Dahl')
    with pytest.raises(AssertionError):
        deepEqual(nb1, nb2)
    with pytest.raises(AssertionError):
        deepEqual('a', {})

def test_throwing():
    def thrower(exc_type):
        raise exc_type('test')
    aethrow = make_block(thrower, AssertionError)
    throws(make_block(thrower, AssertionError), AssertionError)
    throws(make_block(thrower, AssertionError), AssertionError)
    throws(make_block(thrower, AssertionError))
    throws(make_block(thrower, TypeError))
    threw = False
    try:
        throws(make_block(thrower, TypeError), AssertionError)
    except Exception as e:
        threw = True
        ok(isinstance(e, TypeError))
    equal(True, threw)

def test_does_not_throw_should_pass_through():
    def thrower(exc_type):
        raise exc_type('test')
    threw = False
    try:
        doesNotThrow(make_block(thrower, TypeError), AssertionError)
    except Exception as e:
        threw = True
        ok(isinstance(e, TypeError))
    equal(True, threw)
    threw = False
    try:
        doesNotThrow(make_block(thrower, TypeError), TypeError)
    except Exception as e:
        threw = True
        ok(isinstance(e, AssertionError))
    equal(True, threw)

def test_if_error():
    with pytest.raises(Exception):
        ifError(Exception("test error"))
    doesNotThrow(lambda: ifError(None))
    doesNotThrow(lambda: ifError(None))

def test_constructor_validation():
    threw = False
    try:
        throws(lambda: (_ for _ in ()).throw({}), list)
    except:
        threw = True
    ok(threw)

def test_regexp_predicate_validation():
    import re
    throws(lambda: (_ for _ in ()).throw(TypeError("test")), re.compile("test"))
    throws(lambda: (_ for _ in ()).throw(TypeError("test")), lambda err: isinstance(err, TypeError) and "test" in str(err))

def test_circular_refs():
    b = {}
    b["b"] = b
    c = {}
    c["b"] = c
    gotError = False
    try:
        deepEqual(b, c)
    except:
        gotError = True
    ok(gotError)

def test_arguments_reflexivity():
    args = tuple()
    with pytest.raises(Exception):
        deepEqual([], args)
    with pytest.raises(Exception):
        deepEqual(args, [])

def test_assertion_message_generation():
    def check(actual, expected):
        try:
            equal(actual, "")
        except AssertionError as e:
            assert str(e) == f"AssertionError: {expected} == \"\""
            assert e.generatedMessage
    check(None, '"None"')
    check(True, 'True')
    check(False, 'False')
    check(0, '0')
    check(100, '100')
    import math
    check(float('nan'), '"nan"')
    check(float('inf'), '"inf"')
    check(float('-inf'), '"-inf"')
    check("", '""')
    check("foo", '"foo"')
    check([], '[]')
    check([1, 2, 3], '[1, 2, 3]')
    check(repr(re.compile('a')), repr(re.compile('a')))
    check({}, '{}')
    check({'a': None, 'b': None}, "{'a': None, 'b': None}")
    check({'a': float('nan'), 'b': float('inf'), 'c': float('-inf')}, str({'a': float('nan'), 'b': float('inf'), 'c': float('-inf')}))

def test_missing_expected_exception_branch():
    threw = False
    try:
        throws(lambda: ifError(None))
    except AssertionError as e:
        threw = True
        assert e.message == "Missing expected exception.."
    ok(threw)

def test_error_message_correctly_generated_and_custom():
    try:
        equal(1, 2)
    except AssertionError as e:
        assert str(e).split('\n')[0] == 'AssertionError: 1 == 2'
        assert e.generatedMessage

    try:
        equal(1, 2, 'oh no')
    except AssertionError as e:
        assert str(e).split('\n')[0] == 'AssertionError: oh no'
        assert not e.generatedMessage