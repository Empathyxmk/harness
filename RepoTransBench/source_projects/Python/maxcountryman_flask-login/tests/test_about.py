import warnings
import importlib
import sys

def test_about_warns(monkeypatch):
    # Import must trigger a DeprecationWarning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # Reload module to retrigger warning
        if "flask_login.__about__" in sys.modules:
            del sys.modules["flask_login.__about__"]
        import flask_login.__about__ as about
        assert any("deprecated" in str(warn.message).lower() for warn in w)
        # Also check module vars
        assert about.__title__ == "Flask-Login"
        assert about.__version__ == "0.7.0"

def test_init_dunder_version_warns(monkeypatch):
    import flask_login
    # Make sure __version__ returns expected warning and version string
    monkeypatch.setattr("importlib.metadata.version", lambda name: "1.2.3")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        val = flask_login.__version__
        assert val == "1.2.3"
        assert any("deprecated" in str(warn.message).lower() for warn in w)

def test_init_dunder_version_attribute_error():
    import flask_login
    try:
        _ = flask_login.__notarealattr__
    except AttributeError as e:
        assert str(e) == "notarealattr"
    else:
        assert False, "Should raise AttributeError"