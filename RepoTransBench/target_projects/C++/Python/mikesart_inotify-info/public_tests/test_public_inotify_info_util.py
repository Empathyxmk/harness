import pytest
import os

def test_alternate_stat_basic():
    # Public test: struct stat s; s.st_nlink = 42; EXPECT_EQ(s.st_nlink, 42)
    class Stat:
        def __init__(self):
            self.st_nlink = 0

    s = Stat()
    s.st_nlink = 42
    assert s.st_nlink == 42