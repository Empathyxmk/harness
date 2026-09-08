import types
import importlib

def test_public_wsgi_application_type():
    import wsgi
    from werkzeug.wsgi import DispatcherMiddleware
    # Test that `application` is a DispatcherMiddleware instance
    assert isinstance(wsgi.application, DispatcherMiddleware)

def test_public_wsgi_application_mapping():
    import wsgi
    # The application should have a `mounts` attribute mapping '/api'
    assert "/api" in wsgi.application.mounts