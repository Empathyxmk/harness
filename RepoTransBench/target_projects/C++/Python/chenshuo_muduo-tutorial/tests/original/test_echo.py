import sys
import os
import pytest

# Import the echo server code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from echo_server import EventLoop, InetAddress, EchoServer, _TcpConnectionStub

def test_connection_sets_last_connected():
    loop = EventLoop()
    addr = InetAddress(8888)
    server = EchoServer(loop, addr)
    assert server.last_connected_ is False
    server.onConnection()
    assert server.last_connected_ is True

def test_message_echo():
    loop = EventLoop()
    addr = InetAddress(8888)
    server = EchoServer(loop, addr)
    test_msg = "hello, world"
    _TcpConnectionStub.setInputBuffer(test_msg)
    server.onMessage()
    assert server.last_echoed_ == test_msg

def test_echo_server_all():
    # Compound test for flow
    loop = EventLoop()
    addr = InetAddress(8888)
    server = EchoServer(loop, addr)
    # Connect
    assert server.last_connected_ is False
    server.onConnection()
    assert server.last_connected_ is True
    # Message
    test_msg = "hello, world"
    _TcpConnectionStub.setInputBuffer(test_msg)
    server.onMessage()
    assert server.last_echoed_ == test_msg