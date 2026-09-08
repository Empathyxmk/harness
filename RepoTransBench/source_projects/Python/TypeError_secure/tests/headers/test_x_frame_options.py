import pytest
from secure.headers.x_frame_options import XFrameOptions

def test_x_frame_options_defaults():
    xfo = XFrameOptions()
    assert xfo.header_value == "SAMEORIGIN"

def test_set_and_clear_value():
    xfo = XFrameOptions()
    xfo.set("foo")
    assert xfo.header_value == "foo"
    xfo.clear()
    assert xfo.header_value == "SAMEORIGIN"

def test_deny_and_sameorigin_methods():
    xfo = XFrameOptions()
    xfo.deny()
    assert xfo.header_value == "DENY"
    xfo.sameorigin()
    assert xfo.header_value == "SAMEORIGIN"