import pytest

def test_import_webhook_public():
    import cloudconvert.webhook as webhook_mod
    assert hasattr(webhook_mod, "Webhook")

def test_webhook_methods_public():
    import cloudconvert.webhook as webhook_mod
    wh = webhook_mod.Webhook()
    methods = [m for m in dir(wh) if not m.startswith('_')]
    # Just check there is any public method defined
    assert any(callable(getattr(wh, m)) for m in methods)