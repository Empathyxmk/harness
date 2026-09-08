# tests/original/test_spdy_frame.py
import pytest
from src.spdy_frame import SpdyFrame, spdy_frame_init, spdy_frame_parse_header, SPDY_CONTROL_FRAME, SPDY_DATA_FRAME
from src.spdy_data import SpdyData
from src.spdy_error import SPDY_ERROR_NONE

def test_spdy_frame_init():
    frame = SpdyFrame()
    rc = spdy_frame_init(frame)
    assert rc == SPDY_ERROR_NONE
    assert frame.prev is None
    assert frame.next is None
    assert frame._header_parsed == 0

def test_spdy_frame_parse_header_control():
    frame = SpdyFrame()
    buf = b'\x80' # C: {0x80}
    data = SpdyData(buf)
    rc = spdy_frame_parse_header(frame, data)
    assert rc == SPDY_ERROR_NONE
    assert frame.type == SPDY_CONTROL_FRAME

def test_spdy_frame_parse_header_data():
    frame = SpdyFrame()
    buf = b'\x00' # C: {0x00}
    data = SpdyData(buf)
    rc = spdy_frame_parse_header(frame, data)
    assert rc == SPDY_ERROR_NONE
    assert frame.type == SPDY_DATA_FRAME