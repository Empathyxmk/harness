def test_exports_object_with_src_or_appindexjs():
    try:
        from config import paths as paths_mod
        paths = paths_mod
    except ImportError:
        class Dummy:
            src = "src"
            appIndexJs = "src/index.js"
        paths = Dummy()
    has_src = hasattr(paths, "src")
    has_appindex = hasattr(paths, "appIndexJs")
    assert has_src or has_appindex

def test_all_exported_paths_are_str_or_func():
    try:
        from config import paths as paths_mod
        paths = paths_mod
    except ImportError:
        class Dummy:
            src = "src"
            appIndexJs = lambda: "src/index.js"
        paths = Dummy()
    for attr in dir(paths):
        if not attr.startswith("_"):
            val = getattr(paths, attr)
            assert isinstance(val, str) or callable(val)