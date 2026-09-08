import pytest

def ditto(msg):
    # Simulate the echo server response, as per Matlab ditto.m
    return msg

def test_echo_example():
    # An example of a basic echo server roundtrip
    msg = 'Hello WebSocket!'
    echoed = ditto(msg)
    assert echoed == msg