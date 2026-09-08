import pytest

try:
    import src.sprintf as sprintfjs
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
    import sprintf as sprintfjs

sprintf = sprintfjs.sprintf
vsprintf = sprintfjs.vsprintf

def should_throw(format, args, err):
    with pytest.raises(err):
        vsprintf(format, args)

def should_not_throw(format, args):
    try:
        vsprintf(format, args)
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_sprintfjs_public_cache_should_not_throw():
    # Use different strings to stimulate cache
    sprintf('toString')
    sprintf('valueOf')
    should_not_throw('%s', ['testing cache...'])
    should_not_throw('%s', ['does this break?'])

def test_sprintfjs_public_throw_syntaxerror_for_new_placeholders():
    should_throw('%z', [], SyntaxError)
    should_throw('%Y', [], SyntaxError)
    should_throw('%s%%%', [], SyntaxError)
    should_throw('%(foo', [], SyntaxError)
    should_throw('%)foo', [], SyntaxError)
    should_throw('%@s', [], SyntaxError)
    should_throw('%()foo', [], SyntaxError)
    should_throw('%(7)s', [], SyntaxError)

def test_numeric_should_throw_typeerror_for_missing_numbers():
    numeric = list('bcdiefguxX')
    for specifier in numeric:
        fmt = sprintf('%%%s', specifier)
        should_throw(fmt, [], TypeError)

def test_s_should_throw_typeerror_for_null_and_undefined():
    should_throw('%s', [None], TypeError)
    should_throw('%s', [None], TypeError)

def test_d_should_throw_typeerror_for_strings_and_objects():
    should_throw('%d', ['foo'], TypeError)
    should_throw('%d', [{}], TypeError)

def test_should_not_throw_for_valid_specifier_values():
    should_not_throw('%d', [7])
    should_not_throw('%s', ['bar'])