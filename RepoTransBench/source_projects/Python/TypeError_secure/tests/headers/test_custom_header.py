import pytest
from secure.headers.custom_header import CustomHeader

def test_custom_header_init_and_properties():
    ch = CustomHeader("X-Sample-Header", "init-value")
    assert ch.header_name == "X-Sample-Header"
    assert ch.header_value == "init-value"

def test_custom_header_set_chain_and_override():
    ch = CustomHeader("X-Chain", "val1")
    ret = ch.set("val2")
    assert ch.header_value == "val2"
    assert ret is ch

def test_custom_header_set_edge_cases():
    ch = CustomHeader("X-Edge", "start")
    ch.set("")
    assert ch.header_value == ""
    ch.set("123")
    assert ch.header_value == "123"