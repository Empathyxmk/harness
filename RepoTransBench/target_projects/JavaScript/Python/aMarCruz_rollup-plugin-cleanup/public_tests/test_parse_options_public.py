import pytest
from src import parse_options

def setup_function():
    parse_options.js_cleanup_calls.clear()

def teardown_function():
    parse_options.js_cleanup_calls.clear()

def test_returns_correct_defaults_with_unrelated_options_given():
    opts = parse_options.parse_options({'notARealOption': 123})
    assert opts == {
        'comments': 'some',
        'compactComments': True,
        'lineEndings': None,
        'maxEmptyLines': 0,
        'sourcemap': True
    }
    assert not parse_options.js_cleanup_calls

def test_handles_comments_as_string_values():
    assert parse_options.parse_options({'comments': 'none'})['comments'] == 'none'
    assert parse_options.parse_options({'comments': 'all'})['comments'] == 'all'

def test_normalizes_comments_array_with_other_string_and_calls_js_cleanup():
    parse_options.parse_options({'comments': ['license']})
    assert parse_options.js_cleanup_calls
    call = parse_options.js_cleanup_calls[-1]
    assert call[2] == {'comments': ['license'], 'sourcemap': False}

def test_handles_comments_as_a_different_array_and_calls_js_cleanup():
    parse_options.parse_options({'comments': ['copyright']})
    assert parse_options.js_cleanup_calls
    call = parse_options.js_cleanup_calls[-1]
    assert call[2] == {'comments': ['copyright'], 'sourcemap': False}

def test_propagates_other_options_properly_different_values():
    opts = parse_options.parse_options({
        'compactComments': True,
        'lineEndings': '\r',
        'maxEmptyLines': 2,
        'sourceMap': False,
        'sourcemap': False,
        'comments': True
    })
    assert opts['compactComments'] is True
    assert opts['lineEndings'] == '\r'
    assert opts['maxEmptyLines'] == 2
    assert opts['sourcemap'] is False
    assert opts['comments'] == 'all'

def test_handles_both_lineendings_and_normalizeeols_different_values():
    assert parse_options.parse_options({'normalizeEols': '\n'})['lineEndings'] == '\n'
    assert parse_options.parse_options({'lineEndings': '\r\n'})['lineEndings'] == '\r\n'

def test_computes_sourcemap_as_true_if_both_sourceMap_and_sourcemap_true():
    assert parse_options.parse_options({'sourceMap': True, 'sourcemap': True})['sourcemap'] is True
    assert parse_options.parse_options({'sourcemap': True})['sourcemap'] is True