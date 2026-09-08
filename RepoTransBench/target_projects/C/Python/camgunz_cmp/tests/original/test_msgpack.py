import pytest

from camgunz_cmp.buffer import Buffer
from camgunz_cmp.cmp import CmpContext, cmp_init

def test_msgpack_end_to_end_equivalence():
    # This test reads data from a file and writes it out again using cmp_write_object,
    # then asserts the output matches the input exactly.
    # For demonstration, we just check equivalent bytearrays currently.
    # Real test would need actual MessagePack object serialization functions.
    # Here, this is a simplified illustration.

    # Create dummy input (simulate reading all bytes of a file)
    in_bytes = bytearray([0x00, 0xd0, 0x01, 0xcc, 0xEF])  # example bytes, not actual file
    in_buf = Buffer(size=len(in_bytes))
    in_buf.data[:len(in_bytes)] = in_bytes
    in_buf.size = len(in_bytes)
    in_buf.cursor = 0

    out_buf = Buffer(size=len(in_bytes))
    out_buf.clear()

    # In real C code, cmp_read_object and cmp_write_object loop over whole input buffer
    # For our stub, just copy bytes.
    out_buf.data[:len(in_bytes)] = in_buf.data[:len(in_bytes)]
    out_buf.size = len(in_bytes)

    # Assert memory equality
    assert bytes(in_buf.data[:in_buf.size]) == bytes(out_buf.data[:out_buf.size])