import sys
import types
import pytest

def test_requests_oauthlib_init_version_raises(monkeypatch):
    # Simulate requests.__version__ < "2.0.0"
    import importlib

    # Patch requests module with older version
    sys_modules_backup = sys.modules.copy()
    fake_requests = types.SimpleNamespace(__version__="1.9.9")
    sys.modules["requests"] = fake_requests

    import importlib.util
    import importlib.machinery

    # Remove requests_oauthlib from sys.modules cache to force reload
    sys.modules.pop("requests_oauthlib", None)
    sys.modules.pop("requests_oauthlib.__init__", None)

    import importlib
    import pathlib
    init_path = pathlib.Path(__file__).parent.parent / "requests_oauthlib" / "__init__.py"
    spec = importlib.util.spec_from_file_location("requests_oauthlib", str(init_path))
    mod = importlib.util.module_from_spec(spec)

    with pytest.raises(Warning) as e:
        spec.loader.exec_module(mod)
    assert "You are using requests version" in str(e.value)
    sys.modules.clear()
    sys.modules.update(sys_modules_backup)

def test_requests_oauthlib_init_null_handler(monkeypatch):
    # Ensure NullHandler is added (no exception)
    import importlib
    import pathlib
    import types
    sys_modules_backup = sys.modules.copy()

    # Use version >= 2.0.0 to avoid warning
    fake_requests = types.SimpleNamespace(__version__="2.40.0")
    sys.modules["requests"] = fake_requests

    # Remove requests_oauthlib from sys.modules cache to force reload
    sys.modules.pop("requests_oauthlib", None)
    sys.modules.pop("requests_oauthlib.__init__", None)

    init_path = pathlib.Path(__file__).parent.parent / "requests_oauthlib" / "__init__.py"
    spec = importlib.util.spec_from_file_location("requests_oauthlib", str(init_path))
    mod = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(mod)
    # No exception, NullHandler called (covered)
    sys.modules.clear()
    sys.modules.update(sys_modules_backup)

def test_setup_py_version(monkeypatch, tmp_path):
    # Test the setup.py version detection code (happy path and fail path)
    import re, builtins
    from pathlib import Path

    project_root = Path(__file__).parent.parent
    init_py_path = project_root / "requests_oauthlib" / "__init__.py"
    setup_py_path = project_root / "setup.py"

    data = init_py_path.read_text()
    # Should find version
    regex = r'__version__ = ["\']([^"\']*)["\']'
    m = re.search(regex, data)
    assert m.group(1)

    # Simulate missing version raises exception
    bad_init = tmp_path / "__init__.py"
    bad_init.write_text("# no version here!")
    code = setup_py_path.read_text()
    code = code.replace('with open("requests_oauthlib/__init__.py", "r") as f:', f'with open(r"{bad_init}", "r") as f:')
    # Write patched code
    bad_setup = tmp_path / "setup.py"
    bad_setup.write_text(code)

    import importlib.util
    spec = importlib.util.spec_from_file_location("bad_setup", str(bad_setup))
    mod = importlib.util.module_from_spec(spec)
    try:
        with pytest.raises(RuntimeError) as excinfo:
            spec.loader.exec_module(mod)
        assert "No version number found!" in str(excinfo.value)
    finally:
        pass

def test_setup_py_publish(monkeypatch):
    import types
    import sys
    import importlib.util
    import pathlib

    setup_py = pathlib.Path(__file__).parent.parent / "setup.py"
    sys_argv_backup = sys.argv[:]
    sys.argv = ["setup.py", "publish"]

    def fake_system(cmd):
        fake_system_ran.append(cmd)
        return 0

    fake_system_ran = []
    monkeypatch.setattr("os.system", fake_system)
    monkeypatch.setattr("sys.exit", lambda *a, **k: (_ for _ in ()).throw(SystemExit))

    spec = importlib.util.spec_from_file_location("setup", str(setup_py))
    mod = importlib.util.module_from_spec(spec)

    # Should raise SystemExit after publish command is called
    with pytest.raises(SystemExit):
        spec.loader.exec_module(mod)
    assert any("sdist" in cmd for cmd in fake_system_ran)

    sys.argv = sys_argv_backup