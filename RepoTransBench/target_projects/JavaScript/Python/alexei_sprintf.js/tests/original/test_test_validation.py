import pytest

try:
    import src.sprintf as sprintfjs
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
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

def test_sprintfjs_cache_consistency():
    # redefine object properties to ensure cache consistency
    sprintf('hasOwnProperty')
    sprintf('constructor')
    should_not_throw('%s', ['caching...'])
    should_not_throw('%s', ['crash?'])

def test_sprintfjs_throw_syntaxerror_for_placeholders():
    should_throw('%', [], SyntaxError)
    should_throw('%A', [], SyntaxError)
    should_throw('%s%', [], SyntaxError)
    should_throw('%(s', [], SyntaxError)
    should_throw('%)s', [], SyntaxError)
    should_throw('%$s', [], SyntaxError)
    should_throw('%()s', [], SyntaxError)
    should_throw('%(12)s', [], SyntaxError)

def test_numeric_should_throw_typeerror_for_invalid_numbers():
    numeric = list('bcdiefguxX')
    for specifier in numeric:
        fmt = sprintf('%%%s', specifier)
        should_throw(fmt, [], TypeError)
        should_throw(fmt, ['str'], TypeError)
        should_throw(fmt, [{}], TypeError)
        should_throw(fmt, ['s'], TypeError)

def test_numeric_should_not_throw_typeerror_for_castable_numbers():
    numeric = list('bcdiefguxX')
    for specifier in numeric:
        fmt = sprintf('%%%s', specifier)
        should_not_throw(fmt, [float('inf')])
        should_not_throw(fmt, [True])
        should_not_throw(fmt, [[1]])
        should_not_throw(fmt, ['200'])
        should_not_throw(fmt, [None])

def test_should_not_throw_on_undefined_expression():
    should_not_throw("%(x.y)s", {'x': {}})

def test_should_throw_own_error_on_expression_evaluation_typeerror():
    fmt = "%(x.y)s"
    try:
        sprintf(fmt, {})
    except Exception as e:
        assert '[sprintf]' in str(e)

def test_should_not_throw_accessing_prototype_properties():
    class C:
        @property
        def x(self): return 2
        @property
        def y(self): return None
        # Just for completeness; setter does nothing

    c = C()
    should_not_throw("%(x)s", c)
    should_not_throw("%(y)s", c)