import pytest
import zmq

def test_context_socket_version():
    major, minor, patch = zmq.zmq_version_info()
    assert major >= 1
    ctx = zmq.Context(1)
    sock = ctx.socket(zmq.PAIR)
    sock.close()
    ctx.term()

def test_push_pull_lifecycle():
    ctx = zmq.Context(1)
    pull = ctx.socket(zmq.PULL)
    push = ctx.socket(zmq.PUSH)
    # Move push socket (simulate move by creating new reference, delete old)
    moved = push
    # In Python, we don't need manual move semantics; just check usable
    del push
    pull.close()
    moved.close()
    ctx.term()

def test_version_string():
    a, b, c = zmq.zmq_version_info()
    assert a > 0