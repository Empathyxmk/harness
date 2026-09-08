import pytest
from src.parse import parse

def objResult(result):
    # Returns only key:value pairs from parse output, ignoring comments/non-envs
    if isinstance(result, list):
        return {item['key']: item['value'] for item in result if item.get('isEnvVar')}
    return result

def test_public_parse_simple_key_value():
    result = objResult(parse('BAR=foo'))
    assert result == {'BAR': 'foo'}

def test_public_parse_multiple_lines():
    result = objResult(parse('X=100\nY=200'))
    assert result == {'X': '100', 'Y': '200'}

def test_public_trim_whitespace():
    result = objResult(parse('  HELLO =  world  '))
    assert result == {'HELLO': 'world  '}

def test_public_ignore_comments():
    result = parse('# This is a comment\nBAR=foo\n# Another comment')
    found = any(item['key'] == 'BAR' and item['value'] == 'foo' and item['isEnvVar'] for item in result)
    assert found

def test_public_handle_empty_lines():
    result = parse('\nFOO1=abc\n\nFOO2=xyz\n')
    found_foo1 = any(item['key'] == 'FOO1' and item['value'] == 'abc' and item['isEnvVar'] for item in result)
    found_foo2 = any(item['key'] == 'FOO2' and item['value'] == 'xyz' and item['isEnvVar'] for item in result)
    assert found_foo1 and found_foo2

def test_public_ignore_lines_without_equal():
    result = parse('ONE=11\nNO_PAIR\nTWO=22')
    filtered = [x for x in result if x['isEnvVar']]
    assert filtered[0]['key'] == 'ONE' and filtered[0]['value'] == '11'
    assert filtered[1]['key'] == 'TWO' and filtered[1]['value'] == '22'

def test_public_parse_quoted_strings():
    assert objResult(parse('GREETING="hello world"')) == {'GREETING': 'hello world'}

def test_public_handle_equal_within_quoted():
    assert objResult(parse('EQUAL="foo=bar"')) == {'EQUAL': 'foo=bar'}

def test_public_empty_or_whitespace_input():
    result = parse(' ')
    if isinstance(result, list) and len(result) == 1 and result[0].get('isEnvVar') is False:
        assert result[0]['value'] == ''
    else:
        assert result == {}

def test_public_buffer_input():
    data = b'ALPHA=OMEGA\nOMEGA=ALPHA'
    result = objResult(parse(data))
    assert result == {'ALPHA': 'OMEGA', 'OMEGA': 'ALPHA'}

def test_public_single_quoted_strings():
    assert objResult(parse("KEY='single quoted'")) == {'KEY': 'single quoted'}

def test_public_empty_value():
    assert objResult(parse('BAR=')) == {'BAR': ''}

def test_public_whitespace_lines_with_tabs():
    result = parse('\t \n\t')
    assert all(x['isEnvVar'] is False for x in result)

def test_public_value_with_hash_in_quotes():
    assert objResult(parse('BAR="#hashInValue"')) == {'BAR': '#hashInValue'}

def test_public_ignore_trailing_hash_when_not_quoted():
    parsed = parse('BAR=baz # end comment')
    assert parsed[0]['key'] == 'BAR'
    assert parsed[0]['value'] == 'baz '

def test_public_just_comment_is_not_envvar():
    parsed = parse('# nothing here')
    assert parsed[0]['isEnvVar'] is False
    assert parsed[0]['key'] is None

def test_public_keys_with_periods_and_dashes():
    out = parse('X.Y=42\nX-Y=42')
    filtered_keys = [x['key'] for x in out if x['isEnvVar']]
    assert filtered_keys == ['X.Y', 'X-Y']

def test_public_empty_values_with_and_without_quotes():
    out1 = parse('EMPTY1=')
    out2 = parse('EMPTY2=""')
    out3 = parse("EMPTY3=''")
    assert objResult(out1) == {'EMPTY1': ''}
    assert objResult(out2) == {'EMPTY2': ''}
    assert objResult(out3) == {'EMPTY3': ''}

def test_public_malformed_line_is_not_envvar():
    out = parse('=no_key')
    assert out[0]['isEnvVar'] is False
    assert out[0]['key'] is None
    assert isinstance(out[0]['value'], str)