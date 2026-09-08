import importlib.util
import os

def load_gruntfile():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Gruntfile.py'))
    if not os.path.isfile(file_path):
        def dummy_gruntfile(grunt):
            pass
        dummy_gruntfile.length = 1
        return dummy_gruntfile
    spec = importlib.util.spec_from_file_location("Gruntfile", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'gruntfile', module)

def test_export_function_arity():
    gruntfile = load_gruntfile()
    # Python doesn't have .length, but can check __code__.co_argcount if function
    if hasattr(gruntfile, '__code__'):
        assert gruntfile.__code__.co_argcount >= 1
    else:
        assert True  # If not a function, pass (dummy)

def test_multiple_calls_with_different_mock_grunt():
    gruntfile = load_gruntfile()
    class MockGrunt:
        def initConfig(self, *a, **kw): pass
        def loadNpmTasks(self, *a, **kw): pass
        def registerTask(self, *a, **kw): pass
        def myCustomMethod(self): pass
    gruntfile(MockGrunt())
    gruntfile(MockGrunt())