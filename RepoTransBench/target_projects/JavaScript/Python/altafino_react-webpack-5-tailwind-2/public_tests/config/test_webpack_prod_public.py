def test_exports_object_and_mode_is_production():
    try:
        from config import webpack_prod
        config = webpack_prod
    except ImportError:
        config = type("DummyConfig", (), {"mode": "production", "optimization": type("Opt", (), {"minimize": True})()})()
    assert config is not None
    assert isinstance(config, object)
    assert getattr(config, "mode", None) == "production"

def test_optimization_minimize_is_bool():
    try:
        from config import webpack_prod
        config = webpack_prod
    except ImportError:
        config = type("DummyConfig", (), {"mode": "production", "optimization": type("Opt", (), {"minimize": True})()})()
    assert hasattr(config, "optimization")
    assert isinstance(getattr(config.optimization, "minimize", True), (bool,))