from src.util.md5 import (
    md5, MD5Context, md5_init, md5_update_c, md5_final, digest_to_hex,
    md5_starts, md5_update, md5_finish
)
import hashlib

def test_md5_basic():
    msg = b"abc"
    out = bytearray(16)
    md5(msg, len(msg), out)
    expected = hashlib.md5(msg).hexdigest()
    result = digest_to_hex(out)
    assert result == expected, f"MD5('abc') failed. Got: {result}"

def test_md5_empty():
    msg = b""
    out = bytearray(16)
    md5(msg, len(msg), out)
    expected = hashlib.md5(msg).hexdigest()
    result = digest_to_hex(out)
    assert result == expected, f"MD5('') failed. Got: {result}"

def test_md5_chunkwise():
    msg = b"message digest"
    ctx = MD5Context()
    md5_init(ctx)
    md5_update_c(ctx, b"message ", 8)
    md5_update_c(ctx, b"digest", 6)
    digest = bytearray(16)
    md5_final(digest, ctx)
    expected = hashlib.md5(msg).hexdigest()
    result = digest_to_hex(digest)
    assert result == expected, f"MD5(chunked 'message digest') failed. Got: {result}"

def test_md5_restart():
    ctx = MD5Context()
    md5_starts(ctx)
    md5_update(ctx, b"one", 3)
    buf1 = bytearray(16)
    md5_finish(ctx, buf1)

    md5_starts(ctx)
    md5_update(ctx, b"two", 3)
    buf2 = bytearray(16)
    md5_finish(ctx, buf2)

    hex1 = "".join("{:02x}".format(b) for b in buf1)
    hex2 = "".join("{:02x}".format(b) for b in buf2)
    expected1 = hashlib.md5(b"one").hexdigest()
    expected2 = hashlib.md5(b"two").hexdigest()
    assert hex1 == expected1, f'MD5("one") failed (restart). Got: {hex1}'
    assert hex2 == expected2, f'MD5("two") failed (restart). Got: {hex2}'

def test_md5_partial_block():
    msg = b"X" * 55
    output = bytearray(16)
    ctx = MD5Context()
    md5_starts(ctx)
    md5_update(ctx, msg, len(msg))
    md5_finish(ctx, output)
    hexstr = "".join("{:02x}".format(b) for b in output)
    expected = hashlib.md5(msg).hexdigest()
    assert hexstr == expected, f"MD5('X'*55) failed. Got: {hexstr}"

def test_md5_large():
    msg = b"A" * 100000
    output = bytearray(16)
    ctx = MD5Context()
    md5_starts(ctx)
    md5_update(ctx, msg, len(msg))
    md5_finish(ctx, output)
    hexstr = "".join("{:02x}".format(b) for b in output)
    expected = hashlib.md5(msg).hexdigest()
    assert hexstr == expected, f"MD5('A'*100000) failed. Got: {hexstr}"