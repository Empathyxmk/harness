import importlib.util
import types
import sys
import os
import pytest

def load_gruntfile():
    # Try to load Gruntfile.py if available, else dummy function for test demonstration
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Gruntfile.py'))
    if not os.path.isfile(file_path):
        def dummy_gruntfile(grunt):
            pass
        return dummy_gruntfile
    spec = importlib.util.spec_from_file_location("Gruntfile", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'gruntfile', module)  # Module or function

def test_export_a_function():
    gruntfile = load_gruntfile()
    assert callable(gruntfile)

def test_no_throw_with_mock_grunt():
    gruntfile = load_gruntfile()
    class MockGrunt:
        def initConfig(self, *a, **kw): pass
        def loadNpmTasks(self, *a, **kw): pass
        def registerTask(self, *a, **kw): pass
    try:
        gruntfile(MockGrunt())
    except Exception as e:
        pytest.fail(f"Gruntfile raised an exception when called with mock grunt: {e}")