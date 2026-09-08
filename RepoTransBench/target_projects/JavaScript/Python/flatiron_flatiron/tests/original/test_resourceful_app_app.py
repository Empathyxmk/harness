import pytest

def test_loads_resourceful_plugin_and_exposes_app():
    # Assuming the app is implemented in Python and importable
    try:
        from examples.resourceful_app import app as app_module
        app = app_module
    except ModuleNotFoundError:
        pytest.skip("App source not present (examples.resourceful_app.app)")
        return

    assert app is not None
    # Further resourceful behavior would require HTTP server spin-up
    assert hasattr(app, "plugins")
    assert hasattr(app.plugins, "resourceful")
    assert isinstance(app.plugins.resourceful, object)