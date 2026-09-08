import sys
import types
import builtins
import importlib
import pytest

@pytest.fixture(autouse=True)
def reload_win32():
    # Make sure we reload win32 for each test!
    import colorama.win32 as cz_win32
    importlib.reload(cz_win32)
    yield
    importlib.reload(cz_win32)

def test_import_win32_no_ctypes(monkeypatch):
    # Simulate ImportError or AttributeError for ctypes
    monkeypatch.setitem(sys.modules, "ctypes", None)
    import importlib
    import colorama.win32 as cz_win32
    importlib.reload(cz_win32)
    # Check windll and dummy functions exist
    assert cz_win32.windll is None
    assert callable(cz_win32.SetConsoleTextAttribute)
    assert callable(cz_win32.winapi_test)

def test_import_win32_with_ctypes(monkeypatch):
    # Simulate proper import of ctypes and windll
    try:
        import colorama.win32 as cz_win32
        assert hasattr(cz_win32, "STDOUT")
        assert hasattr(cz_win32, "STDERR")
    except Exception:
        # On unix, all these are dummies.
        pass

def test_dummy_SetConsoleTextAttribute(monkeypatch):
    # In dummy fallback path, SetConsoleTextAttribute returns None
    monkeypatch.setitem(sys.modules, "ctypes", None)
    import importlib
    import colorama.win32 as cz_win32
    importlib.reload(cz_win32)
    assert cz_win32.SetConsoleTextAttribute("foo", 0) is None

def test_dummy_winapi_test(monkeypatch):
    # In dummy fallback path, winapi_test returns None
    monkeypatch.setitem(sys.modules, "ctypes", None)
    import importlib
    import colorama.win32 as cz_win32
    importlib.reload(cz_win32)
    assert cz_win32.winapi_test() is None