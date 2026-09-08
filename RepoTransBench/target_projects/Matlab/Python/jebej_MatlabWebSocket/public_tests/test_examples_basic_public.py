import pytest

def ditto(msg):
    return msg

def test_echo_example_public():
    msg = 'Hello from Public!'
    echoed = ditto(msg)
    assert echoed == msg