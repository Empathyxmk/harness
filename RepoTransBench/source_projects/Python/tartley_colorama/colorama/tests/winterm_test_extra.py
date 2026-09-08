from colorama.winterm import WinColor, WinStyle, WinTerm
import pytest

def test_wincolor_constants():
    assert WinColor.BLACK == 0
    assert WinColor.BLUE == 1
    assert WinColor.GREY == 7

def test_winstyle_constants():
    assert WinStyle.BRIGHT | WinStyle.NORMAL >= 0
    assert WinStyle.BRIGHT_BACKGROUND >= 0

def test_get_osfhandle_on_nonwin():
    from colorama import winterm
    if hasattr(winterm, "get_osfhandle"):
        with pytest.raises(OSError):
            winterm.get_osfhandle(1)

def test_win_term_methods(monkeypatch):
    # monkeypatch win32 calls to avoid needing Windows/ctypes
    import colorama.win32 as win32
    monkeypatch.setattr(win32, "GetConsoleScreenBufferInfo", lambda stream_id=None: type("dummy", (), {"wAttributes": 7, "dwCursorPosition": type("dummypos", (), {"X": 1, "Y": 1})()})())
    monkeypatch.setattr(win32, "SetConsoleTextAttribute", lambda *a, **k: None)
    monkeypatch.setattr(win32, "SetConsoleCursorPosition", lambda *a, **k: None)
    term = WinTerm()
    term.set_attrs(15)
    assert isinstance(term.get_attrs(), int)
    term.fore(3)
    term.back(2)
    term.style(1)
    term.set_console(attrs=7)
    pos = type("pos", (), {"X": 1, "Y": 1})()
    term.set_cursor_position(position=pos)
    term.reset_all()