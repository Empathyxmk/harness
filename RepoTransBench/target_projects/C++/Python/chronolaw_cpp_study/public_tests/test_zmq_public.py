import pytest
import zmq
import threading
import time

def test_public_case1_ipc():
    # Use IPC address, as in the source public test
    context = zmq.Context(1)
    addr = "ipc:///tmp/zmq_public.sock"
    msg_value = b"public zmq test"

    def receiver():
        sock = context.socket(zmq.PULL)
        sock.bind(addr)
        msg = sock.recv()
        assert msg == msg_value
        sock.close()

    def sender():
        sock = context.socket(zmq.PUSH)
        sock.connect(addr)
        time.sleep(0.1) # ensure bind happens first
        sock.send(msg_value)
        sock.close()

    recv_thread = threading.Thread(target=receiver)
    recv_thread.start()
    time.sleep(0.05) # let thread bind first
    sender()
    recv_thread.join()
    context.term()

def test_public_case2_tcp():
    # Different TCP port for public test, 5556
    context = zmq.Context(1)
    addr = "tcp://127.0.0.1:5556"

    def server():
        sock = context.socket(zmq.PULL)
        sock.setsockopt(zmq.LINGER, 0)
        sock.setsockopt(zmq.RCVHWM, 1000)
        sock.bind(addr)
        for i in range(2):
            msg = sock.recv()
            msg_str = msg.decode()
            assert msg_str.startswith("pubmsg")
        sock.close()

    def client(i):
        sock = context.socket(zmq.PUSH)
        sock.setsockopt(zmq.SNDHWM, 100)
        sock.connect(addr)
        msg = "pubmsg {}".format(i+100)
        time.sleep(0.1) # allow server bind
        sock.send(msg.encode())
        sock.close()

    server_thread = threading.Thread(target=server)
    server_thread.start()
    time.sleep(0.2)
    c1 = threading.Thread(target=client, args=(0,))
    c2 = threading.Thread(target=client, args=(1,))
    c1.start()
    c2.start()
    c1.join()
    c2.join()
    server_thread.join()
    context.term()