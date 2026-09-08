import pytest

def test_exposes_app_and_has_resourceful_plugin():
    try:
        from examples.resourceful_app import app as app_module
        app = app_module
    except ModuleNotFoundError:
        pytest.skip("App source not present (examples.resourceful_app.app)")
        return

    assert app is not None
    assert hasattr(app, "plugins")
    assert "resourceful" in getattr(app.plugins, "__dict__", app.plugins.__dict__ if hasattr(app.plugins, "__dict__") else [])
    assert getattr(app.plugins, "resourceful", None) is not None