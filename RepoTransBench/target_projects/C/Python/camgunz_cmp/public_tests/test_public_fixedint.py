import pytest

from camgunz_cmp.cmp import CmpContext, cmp_read_u8
from camgunz_cmp.buffer import Buffer

def test_public_fixedint():
    # Simulate C: buf[] = {0xcc, 0xEF}; (MessagePack uint8 239)
    buf_bytes = bytearray([0xcc, 0xEF])
    buf_stub = {'data': buf_bytes}
    ctx = CmpContext(buf_stub)
    val_out = [0]
    assert cmp_read_u8(ctx, val_out)
    assert val_out[0] == 0xEF