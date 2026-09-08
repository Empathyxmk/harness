import pytest

class FakePlugins:
    gradients = lambda *args, **kwargs: None

def test_should_export_gradients_key():
    plugins = FakePlugins()
    assert hasattr(plugins, 'gradients')