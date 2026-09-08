import math

try:
    import src.sprintf as sprintfjs
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
    import sprintf as sprintfjs

sprintf = sprintfjs.sprintf

class DummyRegex:
    # Simulate /<("[^"]*"|'[^']*'|[^'">])*>/ in repr for test
    def __repr__(self):
        return '/<("[^"]*"|\'[^\']*\'|[^\'">])*>/'
    def __str__(self):
        return '/<("[^"]*"|\'[^\']*\'|[^\'">])*>/'

def test_should_return_formatted_strings_for_simple_placeholders():
    pi = math.pi
    assert '%' == sprintf('%%')
    assert '10' == sprintf('%b', 2)
    assert 'A' == sprintf('%c', 65)
    assert '2' == sprintf('%d', 2)
    assert '2' == sprintf('%i', 2)
    assert '2' == sprintf('%d', '2')
    assert '2' == sprintf('%i', '2')
    assert '{"foo":"bar"}' == sprintf('%j', {'foo': 'bar'})
    assert '["foo","bar"]' == sprintf('%j', ['foo', 'bar'])
    assert '2e+0' == sprintf('%e', 2)
    assert '2' == sprintf('%u', 2)
    assert '4294967294' == sprintf('%u', -2)
    assert '2.2' == sprintf('%f', 2.2)
    assert '3.141592653589793' == sprintf('%g', pi)
    assert '10' == sprintf('%o', 8)
    assert '37777777770' == sprintf('%o', -8)
    assert '%s' == sprintf('%s', '%s')
    assert 'ff' == sprintf('%x', 255)
    assert 'ffffff01' == sprintf('%x', -255)
    assert 'FF' == sprintf('%X', 255)
    assert 'FFFFFF01' == sprintf('%X', -255)
    assert 'Polly wants a cracker' == sprintf('%2$s %3$s a %1$s', 'cracker', 'Polly', 'wants')
    assert 'Hello world!' == sprintf('Hello %(who)s!', {'who': 'world'})
    assert 'true' == sprintf('%t', True)
    assert 't' == sprintf('%.1t', True)
    assert 'true' == sprintf('%t', 'true')
    assert 'true' == sprintf('%t', 1)
    assert 'false' == sprintf('%t', False)
    assert 'f' == sprintf('%.1t', False)
    assert 'false' == sprintf('%t', '')
    assert 'false' == sprintf('%t', 0)
    assert 'undefined' == sprintf('%T', None)  # undefined in Python: None
    assert 'null' == sprintf('%T', None)
    assert 'boolean' == sprintf('%T', True)
    assert 'number' == sprintf('%T', 42)
    assert 'string' == sprintf('%T', 'This is a string')
    assert 'function' == sprintf('%T', lambda x: x)
    assert 'array' == sprintf('%T', [1,2,3])
    assert 'object' == sprintf('%T', {'foo':'bar'})
    assert 'regexp' == sprintf('%T', DummyRegex())
    assert 'true' == sprintf('%v', True)
    assert '42' == sprintf('%v', 42)
    assert 'This is a string' == sprintf('%v', 'This is a string')
    assert '1,2,3' == sprintf('%v', [1,2,3])
    assert '[object Object]' == sprintf('%v', {'foo':'bar'})
    assert '/<("[^"]*"|\'[^\']*\'|[^\'">])*>/' == sprintf('%v', DummyRegex())

def test_should_return_formatted_strings_for_complex_placeholders():
    pi = math.pi
    # sign
    assert '2' == sprintf('%d', 2)
    assert '-2' == sprintf('%d', -2)
    assert '+2' == sprintf('%+d', 2)
    assert '-2' == sprintf('%+d', -2)
    assert '2' == sprintf('%i', 2)
    assert '-2' == sprintf('%i', -2)
    assert '+2' == sprintf('%+i', 2)
    assert '-2' == sprintf('%+i', -2)
    assert '2.2' == sprintf('%f', 2.2)
    assert '-2.2' == sprintf('%f', -2.2)
    assert '+2.2' == sprintf('%+f', 2.2)
    assert '-2.2' == sprintf('%+f', -2.2)
    assert '-2.3' == sprintf('%+.1f', -2.34)
    assert '-0.0' == sprintf('%+.1f', -0.01)
    assert '3.14159' == sprintf('%.6g', pi)
    assert '3.14' == sprintf('%.3g', pi)
    assert '3' == sprintf('%.1g', pi)
    assert '-000000123' == sprintf('%+010d', -123)
    assert '______-123' == sprintf("%+'_10d", -123)
    assert '-234.34 123.2' == sprintf('%f %f', -234.34, 123.2)
    # padding
    assert '-0002' == sprintf('%05d', -2)
    assert '-0002' == sprintf('%05i', -2)
    assert '    <' == sprintf('%5s', '<')
    assert '0000<' == sprintf('%05s', '<')
    assert '____<' == sprintf("%'_5s", '<')
    assert '>    ' == sprintf('%-5s', '>')
    assert '>0000' == sprintf('%0-5s', '>')
    assert '>____' == sprintf("%'_-5s", '>')
    assert 'xxxxxx' == sprintf('%5s', 'xxxxxx')
    assert '1234' == sprintf('%02u', 1234)
    assert ' -10.235' == sprintf('%8.3f', -10.23456)
    assert '-12.34 xxx' == sprintf('%f %s', -12.34, 'xxx')
    assert '{\n  "foo": "bar"\n}' == sprintf('%2j', {'foo': 'bar'})
    assert '[\n  "foo",\n  "bar"\n]' == sprintf('%2j', ['foo', 'bar'])
    # precision
    assert '2.3' == sprintf('%.1f', 2.345)
    assert 'xxxxx' == sprintf('%5.5s', 'xxxxxx')
    assert '    x' == sprintf('%5.1s', 'xxxxxx')

def test_should_return_formatted_strings_for_callbacks():
    def cb():
        return 'foobar'
    assert 'foobar' == sprintf('%s', cb)