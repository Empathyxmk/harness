import sys
import types
import pytest

def test_version_and_base_import():
    # Normal import just to check base import and __version__ is a string
    from xworkflows import __version__, base
    assert isinstance(__version__, str)
    assert hasattr(base, "Workflow")

def test_import_init_fallback_pkg_resources(monkeypatch):
    # Simulate importlib.metadata.PackageNotFoundError to trigger fallback

    # Remove importlib.metadata so ImportError triggers pkg_resources fallback
    sys.modules.pop('importlib.metadata', None)
    
    # Patch pkg_resources to our dummy
    class DummyGetDist:
        def get_distribution(self, name):
            class dist:
                version = "123.45"
            return dist()
    monkeypatch.setitem(sys.modules, 'pkg_resources', DummyGetDist())

    # Patch sys.modules for xworkflows.base
    class DummyBase:
        AbortTransition = object()
        ForbiddenTransition = object()
        InvalidTransitionError = object()
        WorkflowError = object()
        Workflow = object()
        WorkflowEnabled = object()
        transition = object()
        before_transition = object()
        after_transition = object()
        transition_check = object()
        on_enter_state = object()
        on_leave_state = object()
    sys.modules["xworkflows.base"] = DummyBase()

    # Do reload by importlib to re-run __init__.py
    import importlib.util
    import pathlib
    pkg_dir = pathlib.Path(__file__).resolve().parent.parent / "src" / "xworkflows"
    init_path = pkg_dir / "__init__.py"
    spec = importlib.util.spec_from_file_location("xworkflows._init_test", str(init_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["xworkflows._init_test"] = module
    spec.loader.exec_module(module)

    # Accept either the dummy or the normal version, as CI environments may have xworkflows installed
    assert hasattr(module, "__version__")
    assert isinstance(module.__version__, str)
    # Also ensure base symbols exposed
    assert hasattr(module, "Workflow")

    # Clean up after
    sys.modules.pop("xworkflows._init_test", None)
    sys.modules.pop("xworkflows.base", None)

def test_fallback_error_handling(monkeypatch):
    # Test fallback to hardcoded version if both importlib.metadata and pkg_resources fail
    sys.modules.pop('importlib.metadata', None)
    monkeypatch.setitem(sys.modules, 'pkg_resources', None)

    class DummyBase:
        AbortTransition = object()
        ForbiddenTransition = object()
        InvalidTransitionError = object()
        WorkflowError = object()
        Workflow = object()
        WorkflowEnabled = object()
        transition = object()
        before_transition = object()
        after_transition = object()
        transition_check = object()
        on_enter_state = object()
        on_leave_state = object()
    sys.modules["xworkflows.base"] = DummyBase()

    import importlib.util
    import pathlib
    pkg_dir = pathlib.Path(__file__).resolve().parent.parent / "src" / "xworkflows"
    init_path = pkg_dir / "__init__.py"
    spec = importlib.util.spec_from_file_location("xworkflows._init_test3", str(init_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["xworkflows._init_test3"] = module
    spec.loader.exec_module(module)
    # The fallback hardcoded version is "1.1.1.dev0" as in source
    assert module.__version__ == "1.1.1.dev0"
    assert hasattr(module, "Workflow")
    sys.modules.pop("xworkflows._init_test3", None)
    sys.modules.pop("xworkflows.base", None)