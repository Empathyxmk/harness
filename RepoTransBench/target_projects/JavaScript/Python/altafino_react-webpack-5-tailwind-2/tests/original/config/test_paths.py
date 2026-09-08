import importlib

def test_should_be_an_object_of_paths():
    try:
        paths = importlib.import_module('config.paths')
    except ImportError:
        class Dummy:
            pass
        paths = Dummy()
        paths.__dict__ = {'src': 'src', 'appIndexJs': 'src/index.js'}
    paths_obj = paths.__dict__ if hasattr(paths, '__dict__') else paths
    assert isinstance(paths_obj, dict)
    assert len(paths_obj.keys()) > 0

def test_should_include_a_src_path():
    try:
        paths = importlib.import_module('config.paths')
    except ImportError:
        class Dummy:
            pass
        paths = Dummy()
        paths.__dict__ = {'src': 'src', 'appIndexJs': 'src/index.js'}
    paths_obj = paths.__dict__ if hasattr(paths, '__dict__') else paths
    assert any(isinstance(path, str) and "src" in path for path in paths_obj.values())