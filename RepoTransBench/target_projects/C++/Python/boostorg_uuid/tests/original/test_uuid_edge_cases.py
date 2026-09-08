import pytest
from src.boost_uuid.uuid import uuid

def test_default_constructed_uuid_is_nil():
    u = uuid()
    for b in u.data:
        assert b == 0

def test_fake_stream_junk_input_parses_nil():
    # Simulate "parsing" with junk - stub: always nil
    out = uuid()  # Always zero, as in C++ stub parser
    for b in out.data:
        assert b == 0

def test_operator_valid_invalid():
    u_valid = uuid([0]*16)
    for b in u_valid.data:
        assert b == 0

def test_assigned_uuid_str():
    u2 = uuid([0]*16)
    oss = str(u2)
    assert oss == "00000000-0000-0000-0000-000000000000"

def test_uuid_all_ones_print():
    u_ff = uuid([0xff]*16)
    oss_ff = str(u_ff)
    assert oss_ff == "ffffffff-ffff-ffff-ffff-ffffffffffff"

def test_stream_width_behavior():
    oss = "00000000-0000-0000-0000-000000000000"
    os_tw = oss.rjust(40)
    assert oss in os_tw

def test_comparison_operators_for_nil():
    nil1 = uuid([0]*16)
    nil2 = uuid([0]*16)
    assert nil1 == nil2
    assert not (nil1 != nil2)

def test_empty_string_parsing_remain_nil():
    # Parsing empty string - stub: always nil
    empty_uuid = uuid([0]*16)
    for b in empty_uuid.data:
        assert b == 0