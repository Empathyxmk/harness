import math
import pytest

try:
    import src.sprintf as sprintfjs
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    import sprintf as sprintfjs

sprintf = sprintfjs.sprintf

class DummyRegex:
    # JavaScript /foo/ → Python: simulate __str__ and __repr__ for test
    def __init__(self, pattern):
        self.pattern = pattern
    def __repr__(self):
        return f"/{self.pattern}/"
    def __str__(self):
        return f"/{self.pattern}/"

def test_should_return_formatted_strings_for_other_simple_placeholders():
    e = math.e
    assert '&' == sprintf('&&'.replace('&', '%%'))  # special escaping test
    assert '101' == sprintf('%b', 5)
    assert 'Z' == sprintf('%c', 90)
    assert '7' == sprintf('%d', 7)
    assert '7' == sprintf('%i', 7)
    assert '42' == sprintf('%d', '42')
    assert '42' == sprintf('%i', '42')
    assert '{"bar":"baz"}' == sprintf('%j', {'bar': 'baz'})
    assert '["bar","baz"]' == sprintf('%j', ['bar', 'baz'])
    assert '3.1e+0' == sprintf('%e', 3.1)
    assert '7' == sprintf('%u', 7)
    assert '4294967291' == sprintf('%u', -5)
    assert '9.8' == sprintf('%f', 9.8)
    assert str(e) == sprintf('%g', e)
    assert '12' == sprintf('%o', 10)
    assert '37777777766' == sprintf('%o', -10)
    assert 'test' == sprintf('%s', 'test')
    assert 'a1' == sprintf('%x', 161)
    assert 'fffffeff' == sprintf('%x', -257)
    assert 'A1' == sprintf('%X', 161)
    assert 'FFFFFEFF' == sprintf('%X', -257)
    assert 'dog jumps over fence' == sprintf('%2$s %3$s over %1$s', 'fence', 'dog', 'jumps')
    assert 'Hello Alex!' == sprintf('Hello %(who)s!', {'who': 'Alex'})
    assert 'false' == sprintf('%t', False)
    assert 'f' == sprintf('%.1t', False)
    assert 'true' == sprintf('%t', 'yes')
    assert 'true' == sprintf('%t', 123)
    assert 'false' == sprintf('%t', 0)
    assert 'f' == sprintf('%.1t', 0)
    # Test for %t false for undefined and null. In Python: None as equivalent
    assert 'false' == sprintf('%t', None) 
    assert 'false' == sprintf('%t', None)
    # Test for NaN, object, types
    assert 'NaN' == sprintf('%T', float('nan'))
    assert 'object' == sprintf('%T', {})
    assert 'number' == sprintf('%T', 12.3)
    assert 'string' == sprintf('%T', 'abcdef')
    assert 'function' == sprintf('%T', lambda x: x)
    assert 'array' == sprintf('%T', [])
    assert 'regexp' == sprintf('%T', DummyRegex("foo"))
    assert 'true' == sprintf('%v', True)
    assert '87' == sprintf('%v', 87)
    assert 'abcdef' == sprintf('%v', 'abcdef')
    assert 'a,b' == sprintf('%v', ['a', 'b'])
    assert '[object Object]' == sprintf('%v', {'a':1})
    assert '/foo/' == sprintf('%v', DummyRegex("foo"))

def test_should_return_formatted_strings_for_other_complex_placeholders():
    e = math.e
    # sign
    assert '5' == sprintf('%d', 5)
    assert '-5' == sprintf('%d', -5)
    assert '+5' == sprintf('%+d', 5)
    assert '-5' == sprintf('%+d', -5)
    assert '9' == sprintf('%i', 9)
    assert '-9' == sprintf('%i', -9)
    assert '+9' == sprintf('%+i', 9)
    assert '-9' == sprintf('%+i', -9)
    assert '4.5' == sprintf('%f', 4.5)
    assert '-4.5' == sprintf('%f', -4.5)
    assert '+4.5' == sprintf('%+f', 4.5)
    assert '-4.5' == sprintf('%+f', -4.5)
    assert '-3.5' == sprintf('%+.1f', -3.46)
    assert '-0.0' == sprintf('%+.1f', -0.001)
    assert '2.71828' == sprintf('%.6g', e)
    assert '2.72' == sprintf('%.3g', e)
    assert '3' == sprintf('%.1g', e)
    assert '-000004567' == sprintf('%+010d', -4567)
    assert '_____-432' == sprintf("%+'_10d", -432)
    assert '-42.50 12.9' == sprintf('%f %f', -42.5, 12.9)
    # padding
    assert '-0012' == sprintf('%05d', -12)
    assert '-0012' == sprintf('%05i', -12)
    assert '    z' == sprintf('%5s', 'z')
    assert '0000z' == sprintf('%05s', 'z')
    assert '____z' == sprintf("%'_5s", 'z')
    assert 'x    ' == sprintf('%-5s', 'x')
    assert 'x0000' == sprintf('%0-5s', 'x')
    assert 'x____' == sprintf("%'_-5s", 'x')
    assert 'abcdef' == sprintf('%5s', 'abcdef')
    assert '0912' == sprintf('%02u', 912)
    assert ' -3.457' == sprintf('%8.3f', -3.4567)
    assert '-5.67 wow' == sprintf('%f %s', -5.67, 'wow')
    assert '{\n  "baz": 1\n}' == sprintf('%2j', {'baz': 1})
    assert '[\n  40,\n  50\n]' == sprintf('%2j', [40, 50])
    # precision
    assert '4.6' == sprintf('%.1f', 4.56)
    assert 'hello' == sprintf('%5.5s', 'hellothere')
    assert '    q' == sprintf('%5.1s', 'queen')

def test_should_return_formatted_strings_for_callbacks():
    def cb():
        return 'bazbat'
    assert 'bazbat' == sprintf('%s', cb)