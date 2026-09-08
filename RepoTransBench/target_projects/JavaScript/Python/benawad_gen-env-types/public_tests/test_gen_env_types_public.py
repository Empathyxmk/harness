from src.gen_env_types import generate_env_types

def test_gen_env_types_different_keys():
    input_str = 'USER=alex\nPASSWORD=secret'
    out = generate_env_types(input_str)
    assert 'declare namespace NodeJS' in out
    assert 'USER: string;' in out
    assert 'PASSWORD: string;' in out

def test_gen_env_types_different_single_key():
    input_str = 'BAR=baz'
    out = generate_env_types(input_str)
    assert 'BAR: string;' in out
    assert 'declare namespace NodeJS' in out

def test_gen_env_types_whitespace_only():
    out = generate_env_types('   ')
    assert 'declare namespace NodeJS' in out
    assert 'interface ProcessEnv' in out

def test_gen_env_types_different_underscores_numbers():
    out = generate_env_types('NAME_2=john\nA3=test')
    assert 'NAME_2: string;' in out
    assert 'A3: string;' in out

def test_gen_env_types_ignore_comment_lines():
    out = generate_env_types('# First comment\nHELLO=world\n# another comment\nWORLD=hello')
    assert 'HELLO: string;' in out
    assert 'WORLD: string;' in out
    assert '#' not in out

def test_gen_env_types_not_include_non_pair():
    out = generate_env_types('ONE=one\nmissingpair\nTWO=two')
    assert 'ONE: string;' in out
    assert 'TWO: string;' in out
    assert 'missingpair' not in out

def test_gen_env_types_empty_value():
    out = generate_env_types('BLANK=')
    assert 'BLANK: string;' in out

def test_gen_env_types_keys_with_dashes_spaces():
    out = generate_env_types('NICE_KEY=good\nBAD-KEY=bad\nKEY WITH SPACE=fail2')
    assert 'NICE_KEY: string;' in out
    assert 'BAD-KEY: string;' not in out
    assert 'KEY WITH SPACE: string;' not in out

def test_gen_env_types_duplicate_keys():
    out = generate_env_types('FOO=abc\nFOO=def\nBAR=xyz')
    assert out.count('FOO: string;') == 1
    assert out.count('BAR: string;') == 1

def test_gen_env_types_skip_invalid_identifier():
    out = generate_env_types('2BAD=shouldskip\n_2GOOD=shouldwork')
    assert '2BAD:' not in out
    assert '_2GOOD: string;' in out

def test_gen_env_types_skip_starting_number():
    out = generate_env_types('99KEY=notype\nTYPE99=has')
    assert '99KEY:' not in out
    assert 'TYPE99: string;' in out

def test_gen_env_types_not_include_keys_with_invalid_characters():
    out = generate_env_types('JUST-KEY=skip\nANOTHER KEY=skip\nDOT.KEY=skip')
    assert 'JUST-KEY:' not in out
    assert 'ANOTHER KEY:' not in out
    assert 'DOT.KEY:' not in out