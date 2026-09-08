import pytest
import os

def test_stat_basic():
    # Test equivalent: struct stat s; s.st_ino = 0; EXPECT_EQ(s.st_ino, 0)
    # In Python, os.stat_result is not assignable, so we create a fake class for demo purpose.
    class Stat:
        def __init__(self):
            self.st_ino = 0

    s = Stat()
    s.st_ino = 0
    assert s.st_ino == 0