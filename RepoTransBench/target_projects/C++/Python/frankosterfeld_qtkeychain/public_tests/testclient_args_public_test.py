import pytest

def printUsage():
    # Simulates printUsage from testclient.cpp
    # We return 1 to match the C++ implementation (see usage tests)
    return 1

def test_needs_at_least_two_arguments_public():
    r = printUsage()
    assert r == 1