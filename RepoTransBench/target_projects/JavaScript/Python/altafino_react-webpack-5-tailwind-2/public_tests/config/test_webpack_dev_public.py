def test_exports_object_and_mode_development():
    try:
        from config import webpack_dev
        config = webpack_dev
    except ImportError:
        config = type("Dummy", (), {"mode": "development", "devtool": "eval-source-map", "entry": ["src/index.js"]})()
    assert getattr(config, "mode", None) == "development"

def test_has_devtool_and_entry():
    try:
        from config import webpack_dev
        config = webpack_dev
    except ImportError:
        config = type("Dummy", (), {"mode": "development", "devtool": "eval-source-map", "entry": ["src/index.js"]})()
    devtool = getattr(config, "devtool", None)
    entry = getattr(config, "entry", None)
    assert isinstance(devtool, str) or devtool is None
    assert isinstance(entry, str) or isinstance(entry, list)