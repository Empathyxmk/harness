from sparts import ctx
import os
import sys

def assert_exists(path):
    assert os.path.exists(path), "Path should exist: %s" % path

def assert_not_exists(path):
    assert not os.path.exists(path), "Path should not exist: %s" % path

def test_public_tmpdir():
    with ctx.tmpdir() as path:
        path_copy = path
        assert_exists(path)
    assert_not_exists(path_copy)

def test_public_add_path():
    with ctx.tmpdir() as path:
        assert path not in sys.path
        with ctx.add_path(path):
            assert path in sys.path
        assert path not in sys.path

def same_path(a, b):
    return os.path.realpath(a) == os.path.realpath(b)

def test_public_chdir():
    with ctx.tmpdir() as path:
        orig_dir = os.getcwd()
        assert not same_path(orig_dir, path)
        with ctx.chdir(path):
            assert same_path(os.getcwd(), path)
        assert not same_path(os.getcwd(), path)
        assert same_path(os.getcwd(), orig_dir)

def test_public_module_snapshot():
    test_name = 'sparts.tests.dummy'
    if test_name in sys.modules:
        sys.modules.pop(test_name)
    assert test_name not in sys.modules
    with ctx.module_snapshot():
        import sparts.tests.dummy
        assert test_name in sys.modules
        assert sys.modules[test_name] is sparts.tests.dummy
    assert test_name not in sys.modules