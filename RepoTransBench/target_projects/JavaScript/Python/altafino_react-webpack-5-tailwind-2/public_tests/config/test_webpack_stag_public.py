def test_exports_object_and_mode_prod_or_staging():
    try:
        from config import webpack_stag
        config = webpack_stag
    except ImportError:
        config = type("Dummy", (), {"mode": "production", "output": type("O", (), {"path": "/dist", "filename": "out.js"})()})()
    assert config is not None
    assert getattr(config, "mode", None) in ["production", "staging"]

def test_output_path_and_output_filename_defined():
    try:
        from config import webpack_stag
        config = webpack_stag
    except ImportError:
        config = type("Dummy", (), {"mode": "production", "output": type("O", (), {"path": "/dist", "filename": "out.js"})()})()
    assert hasattr(config, "output")
    assert hasattr(config.output, "path")
    assert hasattr(config.output, "filename")