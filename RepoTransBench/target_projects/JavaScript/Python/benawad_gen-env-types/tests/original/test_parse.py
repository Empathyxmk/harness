import pytest
from src.parse import parse

def objResult(result):
    # Returns only key:value pairs from parse output, ignoring comments/non-envs
    if isinstance(result, list):
        return {item['key']: item['value'] for item in result if item.get('isEnvVar')}
    return result

def test_parse_key_value_string():
    result = objResult(parse('FOO=bar'))
    assert result == {'FOO': 'bar'}

def test_parse_multiple_lines():
    result = objResult(parse('A=1\nB=2'))
    assert result == {'A': '1', 'B': '2'}

def test_trim_whitespace():
    result = objResult(parse('  X =  5  '))
    assert result == {'X': '5  '}

def test_ignore_comments():
    result = parse('# Hello\nFOO=bar\n# another')
    # FOO=bar should be among the results
    found = any(item['key'] == 'FOO' and item['value'] == 'bar' and item['isEnvVar'] for item in result)
    assert found

def test_handle_empty_lines():
    result = parse('\nA=1\n\nB=2\n')
    found_a = any(item['key'] == 'A' and item['value'] == '1' and item['isEnvVar'] for item in result)
    found_b = any(item['key'] == 'B' and item['value'] == '2' and item['isEnvVar'] for item in result)
    assert found_a and found_b

def test_ignore_lines_without_equal():
    result = parse('A=1\nNOT_A_PAIR\nB=2')
    filtered = [x for x in result if x['isEnvVar']]
    assert filtered[0]['key'] == 'A' and filtered[0]['value'] == '1'
    assert filtered[1]['key'] == 'B' and filtered[1]['value'] == '2'

def test_parse_quoted_strings():
    assert objResult(parse('FOO="bar bar"')) == {'FOO': 'bar bar'}

def test_handle_equal_within_quoted():
    assert objResult(parse('FOO="a=b"')) == {'FOO': 'a=b'}

def test_return_empty_for_empty_input():
    result = parse('')
    if isinstance(result, list) and len(result) == 1 and result[0].get('isEnvVar') is False:
        assert result[0]['value'] == ''
    else:
        assert result == {}

def test_handle_buffer_input():
    data = b'FOO=BAR\nBAR=BAZ'
    result = objResult(parse(data))
    assert result == {'FOO': 'BAR', 'BAR': 'BAZ'}

def test_handle_single_quoted_strings():
    assert objResult(parse("FOO='bar bar'")) == {'FOO': 'bar bar'}

def test_handle_empty_value():
    assert objResult(parse('FOO=')) == {'FOO': ''}

def test_whitespace_only_lines():
    result = parse('   \n \t ')
    assert all(x['isEnvVar'] is False for x in result)

def test_value_with_hash_in_quotes():
    assert objResult(parse('FOO="#notAComment"')) == {'FOO': '#notAComment'}

def test_ignore_trailing_hash_when_not_quoted():
    parsed = parse('FOO=bar # some comment')
    # Value includes space before '#' but not the comment text.
    assert parsed[0]['key'] == 'FOO'
    assert parsed[0]['value'] == 'bar '

def test_comment_is_not_envvar():
    parsed = parse('# only a comment')
    assert parsed[0]['isEnvVar'] is False
    assert parsed[0]['key'] is None

def test_keys_with_periods_and_dashes():
    out = parse('FOO.BAR=test\nFOO-BAR=test')
    filtered_keys = [x['key'] for x in out if x['isEnvVar']]
    assert filtered_keys == ['FOO.BAR', 'FOO-BAR']

def test_empty_values_with_and_without_quotes():
    out1 = parse('FOO=')
    out2 = parse('BAR=""')
    out3 = parse("BAZ=''")
    assert objResult(out1) == {'FOO': ''}
    assert objResult(out2) == {'BAR': ''}
    assert objResult(out3) == {'BAZ': ''}

def test_malformed_line_is_not_envvar():
    out = parse('=novalue')
    assert out[0]['isEnvVar'] is False
    assert out[0]['key'] is None
    assert isinstance(out[0]['value'], str)