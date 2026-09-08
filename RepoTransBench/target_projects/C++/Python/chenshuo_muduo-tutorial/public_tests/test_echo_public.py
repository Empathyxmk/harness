import sys
import os
import pytest

# Import the echo server code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from echo_server import EventLoop, InetAddress, EchoServer, _TcpConnectionStub

def test_connection_sets_last_connected_public():
    loop = EventLoop()
    addr = InetAddress(4321)
    server = EchoServer(loop, addr)
    assert server.last_connected_ is False
    server.onConnection()
    assert server.last_connected_ is True

def test_message_echo_public():
    loop = EventLoop()
    addr = InetAddress(4321)
    server = EchoServer(loop, addr)
    test_msg = "PUBLIC TEST MSG!"
    _TcpConnectionStub.setInputBuffer(test_msg)
    server.onMessage()
    assert server.last_echoed_ == test_msg

def test_echo_server_all_public():
    # Compound test for flow
    loop = EventLoop()
    addr = InetAddress(4321)
    server = EchoServer(loop, addr)
    assert server.last_connected_ is False
    server.onConnection()
    assert server.last_connected_ is True
    test_msg = "PUBLIC TEST MSG!"
    _TcpConnectionStub.setInputBuffer(test_msg)
    server.onMessage()
    assert server.last_echoed_ == test_msg