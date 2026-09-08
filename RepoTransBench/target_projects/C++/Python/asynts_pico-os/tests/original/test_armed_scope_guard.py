import pytest

def test_armedscopeguard():
    i = 0
    # Test using context manager and manual disarm equivalent
    class ArmedScopeGuard:
        def __init__(self, func):
            self.func = func
            self.armed = True

        def disarm(self):
            self.armed = False

        def __del__(self):
            if self.armed:
                self.func()
    # Simulate the C++ test step-by-step
    guard = ArmedScopeGuard(lambda: nonlocal_inc())
    def nonlocal_inc():
        nonlocal i
        i += 1
    guard = ArmedScopeGuard(lambda: nonlocal_inc())
    assert i == 0
    i = 42
    guard.disarm()
    del guard
    assert i == 42
    i = 13
    guard = ArmedScopeGuard(lambda: nonlocal_inc())
    assert i == 13
    del guard
    assert i == 14

def test_armedscopeguard_move():
    i = 0
    # Emulate ownership semantics with explicit cleanup
    class ArmedScopeGuard:
        def __init__(self, func):
            self.func = func
            self.armed = True

        def disarm(self):
            self.armed = False

        def __del__(self):
            if self.armed:
                self.func()
    guard1 = ArmedScopeGuard(lambda: nonlocal_inc())
    def nonlocal_inc():
        nonlocal i
        i += 1
    guard1 = ArmedScopeGuard(lambda: nonlocal_inc())
    assert i == 0
    guard2 = guard1
    guard1 = None    # Move (clear old ref)
    assert i == 0
    guard3 = guard2
    guard2 = None  # Move again
    assert i == 0
    del guard3
    assert i == 1
    assert i == 1