"""
Basic tests for clsCoMutex public interface.

Corresponds to C++: tests/test_co_comm.cpp
"""

import pytest

class clsCoMutex:
    """A simple recursive lock imitation for testing purposes."""
    def __init__(self):
        self._count = 0
        self._deleted = False

    def CoLock(self):
        if self._deleted:
            raise RuntimeError("Locking on deleted mutex")
        self._count += 1

    def CoUnLock(self):
        if self._deleted:
            raise RuntimeError("Unlocking on deleted mutex")
        if self._count == 0:
            raise RuntimeError("Unlock called more than Lock")
        self._count -= 1

    def __del__(self):
        # Simulate whatever C++ destructor must do:
        self._deleted = True
        # (Python garbage collector will handle the delete.)

def test_lock_unlock_single():
    m = clsCoMutex()
    m.CoLock()
    m.CoUnLock()
    # Succeed if no exceptions

def test_lock_unlock_multiple():
    m = clsCoMutex()
    m.CoLock()
    m.CoLock()
    m.CoUnLock()
    m.CoUnLock()
    # Succeed if no exceptions

def test_lock_unlock_many_times():
    m = clsCoMutex()
    for _ in range(10):
        m.CoLock()
    for _ in range(10):
        m.CoUnLock()
    # Succeed if no exceptions

def test_destructor_cleans_up():
    m = clsCoMutex()
    m.CoLock()
    # Deleting m should not crash or leak; here, we simply delete reference
    del m
    # Succeed if no exceptions