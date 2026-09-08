import pytest
import pyzlib

def test_deflate_empty_string():
    compressed, *_ = pyzlib.deflate()(data="", flush_mode='finish')
    assert compressed is not None

def test_inflate_empty_string():
    compressed, *_ = pyzlib.deflate()(data="", flush_mode='finish')
    decompressed = pyzlib.inflate()(compressed, flush_mode='finish')
    assert decompressed == ""

def test_inflate_invalid_fails():
    with pytest.raises(RuntimeError):
        pyzlib.inflate()("notzlibdata")

def test_compress_decompress_1mb():
    big = "a" * 1024 * 1024
    compressed, *_ = pyzlib.deflate()(big, flush_mode='finish')
    decompressed = pyzlib.inflate()(compressed, flush_mode='finish')
    assert decompressed == big