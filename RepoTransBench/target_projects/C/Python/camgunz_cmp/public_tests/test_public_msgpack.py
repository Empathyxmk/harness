import pytest

from camgunz_cmp.cmp import CmpContext, cmp_read_sint
from camgunz_cmp.buffer import Buffer

def test_public_msgpack():
    # Simulate C: buf[0] = 0xd0; buf[1] = 0x81; (MessagePack int8 -127)
    buf_bytes = bytearray([0xd0, 0x81] + [0x00] * 14)
    buf_stub = {'data': buf_bytes}
    ctx = CmpContext(buf_stub)
    val_out = [0]
    assert cmp_read_sint(ctx, val_out)
    assert val_out[0] == -127