# Python equivalent test for index.js function export
import importlib

def test_exports_a_function():
    """
    Equivalent to:
    it('exports a function', () => {
      expect(typeof cookieSession).toBe('function')
    })
    """
    cookie_session = importlib.import_module('src.index')
    # JS default export: require('../index')
    # In Python, check for at least one function export matching expected naming
    exported = [
        getattr(cookie_session, 'default', None),
        getattr(cookie_session, 'cookie_session', None),
        getattr(cookie_session, 'cookieSession', None),
        getattr(cookie_session, '__call__', None)
    ]
    assert any(callable(f) for f in exported), "Expected module to export a function"