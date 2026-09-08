import pytest

from src.incppect import add, strlen_safe, DummyServer

def test_add_works_different_data():
    assert add(2, 2) == 4
    assert add(-10, 5) == -5
    assert add(1000, 2345) == 3345

def test_strlen_safe_different_data():
    assert strlen_safe("abc") == 3
    assert strlen_safe("") == 0
    assert strlen_safe("testing...") == 10
    assert strlen_safe(None) == 0
    assert strlen_safe("a") == 1

def test_dummyserver_serve_and_call_different_data():
    s = DummyServer()
    s.serve("/info", lambda: "Hello")
    assert s.call("/info") == "Hello"
    assert s.call("/info") == "Hello"  # Should be repeatable

def test_dummyserver_overwrite_endpoint_different_data():
    s = DummyServer()
    s.serve("/key", lambda: "value1")
    s.serve("/key", lambda: "value2")
    assert s.call("/key") == "value2"

def test_strlen_safe_partial_different_data():
    str_val = "public-check"
    # For a string, strlen_safe returns len(str), but our C++ test does str length
    import sys
    assert strlen_safe(str_val) == len(str_val)

def test_dummyserver_call_nonexistent_different_data():
    s = DummyServer()
    assert s.call("/doesnotexist") == ""

def test_dummyserver_serve_multiple_endpoints_different_data():
    s = DummyServer()
    s.serve("/a", lambda: "alpha")
    s.serve("/b", lambda: "bravo")
    assert s.call("/a") == "alpha"
    assert s.call("/b") == "bravo"

def test_dummyserver_overwrite_multiple_times_different_data():
    s = DummyServer()
    s.serve("/m", lambda: "1")
    s.serve("/m", lambda: "2")
    s.serve("/m", lambda: "3")
    assert s.call("/m") == "3"