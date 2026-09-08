# Python version of: index.js (public) - should export a function
import importlib

def test_exports_function_type_public():
    """
    Equivalent to:
    it('should export a function type (using toEqual)', () => {
        expect(typeof cookieSession).toEqual('function');
    })
    """
    cookie_session = importlib.import_module('src.index')
    exported = [
        getattr(cookie_session, 'default', None),
        getattr(cookie_session, 'cookie_session', None),
        getattr(cookie_session, 'cookieSession', None),
        getattr(cookie_session, '__call__', None)
    ]
    assert any(callable(f) for f in exported), "Expected public test to confirm function export"