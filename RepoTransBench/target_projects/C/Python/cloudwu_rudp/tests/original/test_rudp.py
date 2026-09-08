import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import rudp
from rudp import MAX_PACKAGE, Rudp, RudpPackage, rudp_new, rudp_delete, rudp_send, rudp_update, rudp_recv

def fill_buffer(buf, sz):
    for i in range(sz):
        buf[i] = i % 100

def test_rudp_new_and_delete():
    U = rudp_new(1, 5)
    assert U is not None
    rudp_delete(U)

def test_rudp_send_and_update_no_recv():
    U = rudp_new(1, 5)
    data = bytearray([1, 2, 3, 4])
    rudp_send(U, data, 4)

    out = rudp_update(U, None, 0, 1)
    # No assertion, just check call succeeds
    rudp_delete(U)

def test_rudp_send_large_package():
    U = rudp_new(1, 5)
    data = bytearray(256)
    fill_buffer(data, 256)
    rudp_send(U, data, 256)

    out = rudp_update(U, None, 0, 1)
    rudp_delete(U)

def test_rudp_recv_corrupt():
    U = rudp_new(1, 5)

    badpacket = bytearray([0xff, 0x00, 0x01, 0x02, 0x03])
    rudp_send(U, badpacket, len(badpacket))
    out = rudp_update(U, None, 0, 1)

    recv_buf = bytearray(MAX_PACKAGE)
    r = rudp_recv(U, recv_buf)
    assert r <= 0
    rudp_delete(U)

def test_rudp_send_update_recv_fuzz():
    U = rudp_new(1, 5)
    payloads = [bytearray([1,2,3,4,5,6]), bytearray([20,30,40,50,60,70]), bytearray([100,101,102,103,104,105])]
    for i in range(3):
        rudp_send(U, payloads[i], 6)

    for t in range(4):
        out = rudp_update(U, None, 0, t)

    rudp_delete(U)

def test_rudp_update_recv_and_recv_edge_cases():
    U = rudp_new(1, 5)
    buf = bytearray([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    rudp_send(U, buf, 16)
    out = rudp_update(U, None, 0, 1)
    if out and hasattr(out, "buffer") and out.sz > 0:
        # Simulate 'wire echo'
        ret = rudp_update(U, out.buffer, out.sz, 2)

    rbuf = bytearray(MAX_PACKAGE)
    r = rudp_recv(U, rbuf)
    rudp_delete(U)

def test_rudp_delete_null_and_empty():
    U = None
    # No rudp_delete(None) as Python would just ignore
    U = rudp_new(1, 5)
    rudp_delete(U)

def test_multiple_queues_and_expiry():
    U = rudp_new(0, 1)
    buf = bytearray([42]*64)
    for i in range(40):
        rudp_send(U, buf, len(buf))
    for t in range(20):
        out = rudp_update(U, None, 0, t)
    rudp_delete(U)