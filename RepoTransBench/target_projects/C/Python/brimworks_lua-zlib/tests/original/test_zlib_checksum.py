import pytest
import pyzlib

def test_adler32_correct_value():
    data = "hello"
    ad = pyzlib.adler32(data)
    assert ad == 92507769, f"adler32('hello') expected 92507769, got {ad}"

def test_crc32_correct_value():
    data = "hello"
    crc = pyzlib.crc32(data)
    assert crc == 907060870, f"crc32('hello') expected 907060870, got {crc}"

def test_adler32_empty_string():
    ad_empty = pyzlib.adler32("")
    assert ad_empty == 1, f"adler32('') expected 1, got {ad_empty}"

def test_crc32_empty_string():
    crc_empty = pyzlib.crc32("")
    assert crc_empty == 0, f"crc32('') expected 0, got {crc_empty}"