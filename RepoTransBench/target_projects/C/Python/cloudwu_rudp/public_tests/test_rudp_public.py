import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import rudp
from rudp import RudpPacket, rudp_seq_incr, rudp_seq_diff, rudp_seq_cmp, rudp_encode_packet, rudp_decode_packet

def test_rudp_seq_incr_public():
    seq = 987654
    res = rudp_seq_incr(seq)
    assert res == 987655

def test_rudp_seq_diff_simple_public():
    a = 3000
    b = 1000
    diff = rudp_seq_diff(a, b)
    assert diff == 2000

def test_rudp_seq_diff_wrap_public():
    a = 10
    b = 4294967290  # UINT32_MAX - 5 + 1
    diff = rudp_seq_diff(a, b)
    assert diff == 16

def test_rudp_seq_cmp_equal_public():
    a = 555555
    b = 555555
    cmpv = rudp_seq_cmp(a, b)
    assert cmpv == 0

def test_rudp_seq_cmp_ahead_public():
    a = 9001
    b = 123
    cmpv = rudp_seq_cmp(a, b)
    assert cmpv == 1

def test_rudp_seq_cmp_behind_public():
    a = 1234
    b = 5678
    cmpv = rudp_seq_cmp(a, b)
    assert cmpv == -1

def test_rudp_encode_decode_basic_public():
    buf = bytearray(64)
    p = RudpPacket()
    p.seq = 1000
    p.ack = 10
    p.flag = 2
    p.data = b"abc"
    p.len = len(p.data)
    length = rudp_encode_packet(p, buf, len(buf))
    assert length > 0

    out = RudpPacket()
    decode_len = rudp_decode_packet(out, buf, length)
    assert decode_len == length

    assert out.seq == 1000
    assert out.ack == 10
    assert out.flag == 2
    assert out.len == 3
    assert out.data == b"abc"

def test_rudp_encode_decode_nontrivial_public():
    buf = bytearray(128)
    p = RudpPacket()
    p.seq = 5555
    p.ack = 2121
    p.flag = 3
    p.data = b"public-12345!!"
    p.len = len(p.data)
    length = rudp_encode_packet(p, buf, len(buf))
    assert length > 0

    out = RudpPacket()
    decode_len = rudp_decode_packet(out, buf, length)
    assert decode_len == length

    assert out.seq == 5555
    assert out.ack == 2121
    assert out.flag == 3
    assert out.len == len(b"public-12345!!")
    assert out.data == b"public-12345!!"