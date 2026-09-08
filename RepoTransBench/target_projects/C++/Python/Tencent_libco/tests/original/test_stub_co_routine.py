"""
Minimal stub implementations for unresolved coroutine symbols required for linking.

Corresponds to C++: tests/test_stub_co_routine.cpp
"""

import pytest

# Mocks for coroutine-related objects (since C++ just stubs them)

class StCoCond:
    # Dummy placeholder for stCoCond_t*
    pass

def co_cond_alloc():
    # Return a dummy instance of StCoCond (like C++ dummy buffer)
    return StCoCond()

def co_cond_free(_):
    return 0

def co_cond_signal(_):
    return 0

def co_cond_timedwait(_, __):
    # Simulate immediate success
    return 0

def co_enable_hook_sys():
    pass

def test_co_cond_alloc_returns_dummy():
    cond = co_cond_alloc()
    assert isinstance(cond, StCoCond)

def test_co_cond_free_returns_zero():
    cond = co_cond_alloc()
    assert co_cond_free(cond) == 0

def test_co_cond_signal_returns_zero():
    cond = co_cond_alloc()
    assert co_cond_signal(cond) == 0

def test_co_cond_timedwait_returns_zero():
    cond = co_cond_alloc()
    assert co_cond_timedwait(cond, 123) == 0

def test_co_enable_hook_sys_does_nothing():
    # Should not raise
    co_enable_hook_sys()