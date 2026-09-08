import pytest

# Simulate src/init.c (basic call tracking for code coverage)
initted = -123

def init():
    global initted
    initted = 42

def test_init_public_call():
    global initted
    initted = -7
    init()
    assert initted == 42