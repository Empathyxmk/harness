# Public test: cookie-session should export a non-null value
import importlib

def test_exports_non_null():
    """
    Equivalent to:
    it('should export a non-null value', () => {
        expect(cookieSession).not.toBeNull();
    })
    """
    cookie_session = importlib.import_module('src.index')
    assert cookie_session is not None