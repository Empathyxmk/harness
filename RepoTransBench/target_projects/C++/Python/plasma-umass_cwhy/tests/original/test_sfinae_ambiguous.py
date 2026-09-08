import sys

def f(arg):
    if isinstance(arg, type(None)):
        print("f(void*)")
    elif isinstance(arg, (bytes, bytearray)):
        print("f(char*)")
    else:
        # Just to make sure we behave deterministically
        print("f(void*)")

def g(t):
    f(t)

def test_g_void_ptr(capsys):
    vp = None
    g(vp)
    captured = capsys.readouterr().out
    assert "f(void*)" in captured

def test_g_char_ptr(capsys):
    buf = bytearray(1)
    g(buf)
    captured = capsys.readouterr().out
    assert "f(char*)" in captured