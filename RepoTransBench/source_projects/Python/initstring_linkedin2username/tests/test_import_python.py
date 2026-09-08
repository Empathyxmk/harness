# This file checks that pytest, coverage, and stdlib are importable and no sys.path/test collection issues exist.
def test_basic_imports():
    import os
    import sys
    import pytest
    import coverage
    assert True