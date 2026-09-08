import types
import pytest
from flask_redis import client

class DummyRedis:
    called_with_url = None
    called_with_kwargs = None

    @classmethod
    def from_url(cls, url, **kwargs):
        cls.called_with_url = url
        cls.called_with_kwargs = kwargs
        class DummyConn:
            pass
        return DummyConn()

def test_init_app_custom_url_public(monkeypatch):
    # Use a different config prefix and a different redis URL
    instance = client.FlaskRedis(strict=False, config_prefix="FOO")
    dummy_app = types.SimpleNamespace()
    dummy_app.config = {"FOO_URL": "redis://localhost:6380/2"}
    setattr(dummy_app, "extensions", {})
    monkeypatch.setattr(instance, "provider_class", DummyRedis)
    instance.init_app(dummy_app, password="letmein")
    assert DummyRedis.called_with_url == "redis://localhost:6380/2"
    assert DummyRedis.called_with_kwargs["password"] == "letmein"
    assert "foo" in dummy_app.extensions
    assert dummy_app.extensions["foo"] is instance

def test_from_custom_provider_public(monkeypatch):
    # Use a unique provider type
    class CustomProvider:
        @staticmethod
        def from_url(url, **kwargs):
            CustomProvider.last_url = url
            CustomProvider.last_kwargs = kwargs
            return "custom-conn"
    dummy_app = types.SimpleNamespace()
    dummy_app.config = {"REDIS_URL": "redis://localhost:6381/4"}
    setattr(dummy_app, "extensions", {})
    instance = client.FlaskRedis.from_custom_provider(CustomProvider, app=dummy_app, fooopt=99)
    assert CustomProvider.last_url == "redis://localhost:6381/4"
    assert CustomProvider.last_kwargs["fooopt"] == 99
    assert "redis" in dummy_app.extensions
    assert dummy_app.extensions["redis"] is instance