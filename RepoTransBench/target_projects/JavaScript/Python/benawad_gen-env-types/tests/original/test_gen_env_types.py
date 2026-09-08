from src.gen_env_types import generate_env_types

def test_generate_env_types_for_keys():
    input_str = 'A=1\nB=2'
    out = generate_env_types(input_str)
    assert 'declare namespace NodeJS' in out
    assert 'A: string;' in out
    assert 'B: string;' in out

def test_single_key():
    input_str = 'FOO=bar'
    out = generate_env_types(input_str)
    assert 'FOO: string;' in out
    assert 'declare namespace NodeJS' in out

def test_valid_ts_when_empty():
    out = generate_env_types('')
    assert 'declare namespace NodeJS' in out
    assert 'interface ProcessEnv' in out

def test_keys_with_numbers_and_underscores():
    out = generate_env_types('FOO_1=hello\nB2=foo')
    assert 'FOO_1: string;' in out
    assert 'B2: string;' in out

def test_ignore_comment_lines():
    out = generate_env_types('# Hello\nFOO=1\n# again\nBAR=2')
    assert 'FOO: string;' in out
    assert 'BAR: string;' in out
    assert '#' not in out

def test_not_include_lines_without_pair():
    out = generate_env_types('FOO=bar\nnotapair\nBAR=baz')
    assert 'FOO: string;' in out
    assert 'BAR: string;' in out
    assert 'notapair' not in out

def test_support_empty_value():
    out = generate_env_types('EMPTY=')
    assert 'EMPTY: string;' in out

def test_handle_keys_with_dashes_or_spaces():
    out = generate_env_types('GOOD_KEY=ok\nBAD-KEY=bad\nKEY WITH SPACE=fail')
    assert 'GOOD_KEY: string;' in out
    assert 'BAD-KEY: string;' not in out
    assert 'KEY WITH SPACE: string;' not in out

def test_duplicate_keys_only_once():
    out = generate_env_types('FOO=1\nFOO=2\nBAR=3')
    assert out.count('FOO: string;') == 1
    assert out.count('BAR: string;') == 1

def test_skip_key_not_valid_identifier():
    out = generate_env_types('1BAD=fail\n_1GOOD=ok')
    assert '1BAD:' not in out
    assert '_1GOOD: string;' in out

def test_key_with_only_numbers_skipped():
    out = generate_env_types('123KEY=fail\nKEY123=ok')
    assert '123KEY:' not in out
    assert 'KEY123: string;' in out

def test_not_include_keys_with_invalid_characters():
    out = generate_env_types('MY-KEY=bad\nMY KEY=bad\nMY.KEY=bad')
    assert 'MY-KEY:' not in out
    assert 'MY KEY:' not in out
    assert 'MY.KEY:' not in out