import pytest

# Simulate src/init.c (basic call tracking for code coverage)
initted = 0

def init():
    global initted
    initted = 1

def test_init_call():
    global initted
    initted = 0
    init()
    assert initted == 1