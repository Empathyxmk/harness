import sys
import types
import pytest

def test_version_and_base_import_public():
    from xworkflows import __version__, base
    assert isinstance(__version__, str)
    # Check existence of a different base symbol from main test
    assert hasattr(base, "WorkflowEnabled")

def test_import_init_fallback_pkg_resources_public(monkeypatch):
    # Remove importlib.metadata so ImportError triggers pkg_resources fallback
    sys.modules.pop('importlib.metadata', None)
    
    # Patch pkg_resources to dummy
    class DummyGetDist:
        def get_distribution(self, name):
            class dist:
                version = "987.65"
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

    import importlib.util
    import pathlib
    pkg_dir = pathlib.Path(__file__).resolve().parent.parent / "src" / "xworkflows"
    init_path = pkg_dir / "__init__.py"
    spec = importlib.util.spec_from_file_location("xworkflows._init_pub_test", str(init_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["xworkflows._init_pub_test"] = module
    spec.loader.exec_module(module)

    assert hasattr(module, "__version__")
    assert isinstance(module.__version__, str)
    assert hasattr(module, "ForbiddenTransition")

    sys.modules.pop("xworkflows._init_pub_test", None)
    sys.modules.pop("xworkflows.base", None)

def test_fallback_error_handling_public(monkeypatch):
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
    spec = importlib.util.spec_from_file_location("xworkflows._init_pub_test2", str(init_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules["xworkflows._init_pub_test2"] = module
    spec.loader.exec_module(module)

    assert module.__version__ == "1.1.1.dev0"
    assert hasattr(module, "InvalidTransitionError")
    sys.modules.pop("xworkflows._init_pub_test2", None)
    sys.modules.pop("xworkflows.base", None)