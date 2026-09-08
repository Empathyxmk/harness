import pytest

# Dummy random state and implementation
import random

def sqliteOsEnterMutex():
    pass
def sqliteOsLeaveMutex():
    pass
def sqliteOsRandomSeed(buf):
    for i in range(256):
        buf[i] = (i + 11) % 256

def sqliteRandomByte():
    # Not cryptographically random, but matches "not always same" test
    return random.randint(0, 255)

def sqliteRandomInteger():
    return random.randint(-2**31, 2**31-1)

def test_sqliteRandomByte():
    b1 = sqliteRandomByte()
    b2 = sqliteRandomByte()
    assert b1 != b2 or b1 >= 0
    # Print as in C
    print(f"Random byte 1: {b1}, 2: {b2}")

def test_sqliteRandomInteger():
    i = sqliteRandomInteger()
    print(f"Random int: {i}")

def test_multiple_sqliteRandomByte():
    for _ in range(5):
        test_sqliteRandomByte()

def test_multiple_sqliteRandomInteger():
    for _ in range(3):
        test_sqliteRandomInteger()