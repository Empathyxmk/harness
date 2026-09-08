import types
import pytest
from flask_redis import client as uut

class DummyRedis:
    url = None
    kwargs = None

    @classmethod
    def from_url(cls, url, **kwargs):
        cls.url = url
        cls.kwargs = kwargs
        class DummyConn:
            pass
        return DummyConn()

def test_flaskredis_init_app_different_url(monkeypatch):
    # Use different config prefix and redis URL from the original private test
    r = uut.FlaskRedis(strict=False, config_prefix="APP2")
    app = types.SimpleNamespace()
    app.config = {"APP2_URL": "redis://127.0.0.1:6382/5"}
    setattr(app, "extensions", {})
    monkeypatch.setattr(r, "provider_class", DummyRedis)
    r.init_app(app, foo="barbazquux")
    assert DummyRedis.url == "redis://127.0.0.1:6382/5"
    assert DummyRedis.kwargs["foo"] == "barbazquux"
    assert "app2" in app.extensions
    assert app.extensions["app2"] is r

def test_from_custom_provider_diff_url(monkeypatch):
    # Use a different provider and redis URL from original tests
    class OtherProvider:
        @staticmethod
        def from_url(url, **kwargs):
            OtherProvider.called_url = url
            OtherProvider.called_kwargs = kwargs
            return "hello-ext"
    app = types.SimpleNamespace()
    app.config = {"REDIS_URL": "redis://192.168.1.2:6399/6"}
    setattr(app, "extensions", {})
    r = uut.FlaskRedis.from_custom_provider(OtherProvider, app=app, baropt="bartest99")
    assert OtherProvider.called_url == "redis://192.168.1.2:6399/6"
    assert OtherProvider.called_kwargs["baropt"] == "bartest99"
    assert "redis" in app.extensions
    assert app.extensions["redis"] is r

def test_flaskredis_basic_instance(monkeypatch):
    # Tests a different config_prefix, checks the instance setup/fields
    r = uut.FlaskRedis(strict=True, config_prefix="BAR")
    assert r.config_prefix == "BAR"
    assert hasattr(r, "from_custom_provider")
    assert hasattr(r, "provider_class")