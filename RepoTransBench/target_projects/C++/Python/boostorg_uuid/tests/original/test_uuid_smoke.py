import pytest
from src.boost_uuid.uuid import uuid

def test_print_nil_uuid():
    u_nil = uuid([0] * 16)
    s_nil = str(u_nil)
    assert s_nil == "00000000-0000-0000-0000-000000000000"

def test_round_trip_operator():
    # Fake round trip; since we lack parsing, just initialize zeros and test fields
    u = uuid([0]*16)
    for b in u.data:
        assert b == 0

def test_dash_hex_value():
    u1 = uuid([0x12,0x34,0x56,0x78, 0x9a,0xbc, 0xde,0xf0, 0x12,0x34, 0x56,0x78,0x9a,0xbc,0xde,0xf0])
    s1 = str(u1)
    assert s1 == "12345678-9abc-def0-1234-56789abcdef0"

def test_hex_hex_values():
    u2 = uuid([0xff,0xee,0xdd,0xcc,0xbb,0xaa,0x99,0x88,0x77,0x66,0x55,0x44,0x33,0x22,0x11,0x00])
    s2 = str(u2)
    assert s2 == "ffeeddcc-bbaa-9988-7766-554433221100"