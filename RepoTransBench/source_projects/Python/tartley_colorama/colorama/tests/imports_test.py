# Direct import/attribute tests for colorama/__init__.py

def test_init_imports():
    import colorama
    assert hasattr(colorama, "init")
    assert hasattr(colorama, "deinit")
    assert hasattr(colorama, "colorama_text")
    assert hasattr(colorama, "just_fix_windows_console")
    assert hasattr(colorama, "__version__")
    assert hasattr(colorama, "AnsiToWin32")
    assert hasattr(colorama, "Fore")
    assert hasattr(colorama, "Back")
    assert hasattr(colorama, "Style")
    assert hasattr(colorama, "Cursor")