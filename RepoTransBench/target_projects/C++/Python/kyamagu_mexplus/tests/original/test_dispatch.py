import pytest

def test_dispatch():
    # In C++ this was just empty functions to test that registration works,
    # in Python, just calling and passing (no actual logic)
    def foo(*args, **kwargs):
        return None
    def bar(*args, **kwargs):
        return None
    foo()
    bar()