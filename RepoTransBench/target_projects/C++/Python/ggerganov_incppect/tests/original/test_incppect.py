import pytest

from src.incppect import add, strlen_safe, DummyServer

def test_add_works():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_strlen_safe():
    assert strlen_safe("") == 0
    assert strlen_safe("abc") == 3
    assert strlen_safe(None) == 0
    assert strlen_safe("longer string") == 13

def test_dummyserver_serve_and_call():
    s = DummyServer()
    s.serve("/foo", lambda: "bar")
    assert s.call("/foo") == "bar"
    assert s.call("/unknown") == ""

def test_dummyserver_overwrite_endpoint():
    s = DummyServer()
    s.serve("/foo", lambda: "one")
    s.serve("/foo", lambda: "two")
    assert s.call("/foo") == "two"

def test_strlen_safe_partial():
    arr = ['a', 'b', 'c', 'd', '\0']
    # As a string, below test cannot be directly replicated; simulate with string, simulate C-array
    # strlen_safe should return 4
    assert strlen_safe(arr) == 4

def test_dummyserver_call_nonexistent():
    s = DummyServer()
    assert s.call("/none") == ""

def test_dummyserver_serve_multiple_endpoints():
    s = DummyServer()
    s.serve("/a", lambda: "A")
    s.serve("/b", lambda: "B")
    assert s.call("/a") == "A"
    assert s.call("/b") == "B"

def test_dummyserver_overwrite_multiple_times():
    s = DummyServer()
    s.serve("/x", lambda: "1")
    s.serve("/x", lambda: "2")
    s.serve("/x", lambda: "3")
    assert s.call("/x") == "3"