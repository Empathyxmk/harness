import pytest
from flask_redis import client as uut

class DummyRedis:
    def __init__(self):
        self.values = {}
    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()
    def __getattr__(self, name):
        if name == "test_func":
            return lambda: "called"
        raise AttributeError(name)
    def __getitem__(self, name):
        return self.values.get(name, None)
    def __setitem__(self, name, value):
        self.values[name] = value
    def __delitem__(self, name):
        del self.values[name]

def test_from_custom_provider_sets_provider_and_inits(monkeypatch):
    class DummyProvider:
        from_url_called = False
        @classmethod
        def from_url(cls, url, **kwargs):
            cls.from_url_called = True
            return DummyRedis()
    app = type("App", (), {"config": {}})()
    inst = uut.FlaskRedis.from_custom_provider(DummyProvider, app)
    assert inst.provider_class == DummyProvider
    assert DummyProvider.from_url_called

def test_from_custom_provider_no_app():
    class DummyProvider:
        pass
    result = uut.FlaskRedis.from_custom_provider(DummyProvider)
    assert result.provider_class is DummyProvider

def test_from_custom_provider_assertion():
    with pytest.raises(AssertionError):
        uut.FlaskRedis.from_custom_provider(None)

def test_dunder_methods_forward(monkeypatch):
    dummy = DummyRedis()
    inst = uut.FlaskRedis()
    inst._redis_client = dummy
    # __getattr__
    assert inst.__getattr__("test_func")() == "called"
    # __getitem__ / __setitem__ / __delitem__
    inst["foo"] = "bar"
    assert inst["foo"] == "bar"
    del inst["foo"]
    assert inst["foo"] is None

def test_init_app_sets_extensions_dict(monkeypatch):
    inst = uut.FlaskRedis()
    inst.provider_class = DummyRedis
    inst.provider_kwargs = {}
    app = type("App", (), {"config": {}, "extensions": {}})()
    inst.init_app(app)
    assert "redis" in app.extensions
    assert app.extensions["redis"] is inst

def test_init_app_creates_extensions(monkeypatch):
    inst = uut.FlaskRedis()
    inst.provider_class = DummyRedis
    inst.provider_kwargs = {}
    class AppObj:
        config = {}
    app = AppObj()
    if hasattr(app, "extensions"):
        delattr(app, "extensions")
    inst.init_app(app)
    assert hasattr(app, "extensions")
    assert "redis" in app.extensions

def test_unusual_config_prefix(monkeypatch):
    inst = uut.FlaskRedis(config_prefix="FOOBAR")
    inst.provider_class = DummyRedis
    inst.provider_kwargs = {}
    app = type("App", (), {"config": {"FOOBAR_URL": "redis://notreal:1234"}, "extensions": {}})()
    inst.init_app(app)
    assert "foobar" in app.extensions
    assert app.extensions["foobar"] is inst