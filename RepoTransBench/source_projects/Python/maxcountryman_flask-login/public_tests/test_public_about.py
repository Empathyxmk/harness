import warnings
import importlib
import sys

def test_about_warns_public(monkeypatch):
    # Import must trigger a DeprecationWarning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # Reload module to retrigger warning
        if "flask_login.__about__" in sys.modules:
            del sys.modules["flask_login.__about__"]
        import flask_login.__about__ as about
        assert any("deprecated" in str(warn.message).lower() for warn in w)
        # Also check module vars (use different checks)
        assert hasattr(about, "__title__")
        assert "Flask" in about.__title__
        assert isinstance(about.__version__, str) and len(about.__version__.split(".")) == 3

def test_init_dunder_version_warns_public(monkeypatch):
    import flask_login
    # Make sure __version__ returns expected warning and version-like string
    monkeypatch.setattr("importlib.metadata.version", lambda name: "2.0.1")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        val = flask_login.__version__
        assert val == "2.0.1"
        assert any("deprecated" in str(warn.message).lower() for warn in w)

def test_init_dunder_version_attribute_error_public():
    import flask_login
    name = "certainlynotanattribute"
    try:
        _ = getattr(flask_login, name)
    except AttributeError as e:
        assert str(e) == name
    else:
        assert False, "Should raise AttributeError"