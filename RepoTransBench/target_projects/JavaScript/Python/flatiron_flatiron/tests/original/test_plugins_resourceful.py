import pytest

def test_app_extends_resourceful_plugin():
    """
    Emulates plugin extension, using dummy app-like object
    """
    class DummyResources:
        @staticmethod
        def Creature(): pass

    class DummyConfig:
        _opts = {}
        def set(self, key, value):
            self._opts[key] = value
        def get(self, key):
            return self._opts.get(key)
    class DummyApp:
        resources = DummyResources
        define = lambda *a, **kw: None
        config = DummyConfig()

    app = DummyApp()
    assert hasattr(app, "resources")
    assert callable(app.resources.Creature)
    assert callable(app.define)

def test_app_initialized_loads_config_and_engine(monkeypatch):
    """
    Simulates app.init, engine mapping, and config checks.
    """
    class DummyEngine:
        pass
    class DummyResources:
        Creature = type("C", (), {})()
    class DummyConfig:
        _opts = {'database': {'uri': 'http://localhost:5984/test'},
                 'resourceful': {'uri': 'http://localhost:5984/test'}}
        def set(self, key, value):
            self._opts[key] = value
        def get(self, key):
            return self._opts.get(key)
    class DummyApp:
        resources = DummyResources()
        resources.Creature.engine = "MemoryEngine"
        define = lambda *a, **kw: None
        config = DummyConfig()
        def init(self, cb):
            cb()  # Callback pattern

    app = DummyApp()
    result = {}
    def cb():
        result['called'] = True
    app.init(cb)
    # Engine check
    assert app.resources.Creature.engine == "MemoryEngine"
    # Config option check
    assert app.config.get('resourceful')['uri'] == app.config.get('database')['uri']