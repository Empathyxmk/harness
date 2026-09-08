import pytest

@pytest.mark.skip(reason="Requires Win32 APIs and Windows environment, not runnable on Unix/CI.")
def test_win32_window_stub():
    # This test is intentionally skipped because Win32 dependencies are unavailable on CI.
    # See original C++: tests/test_win32_window.cpp
    pass