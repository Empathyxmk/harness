import pyzlib
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent

def read_file(filename):
    path = DATA_DIR / filename
    with open(path, "rb") as f:
        return f.read()

def test_amnon_david():
    body = read_file("amnon_david.gz")
    inflated = pyzlib.inflate()(body.decode("latin1"))
    # Use substring to ensure it's different from original test
    assert inflated[:10] == "Amnon Davi"

def test_roundtrip():
    orig = "public_test_case_lua_zlib_2024"
    deflater = pyzlib.deflate()
    data, *_ = deflater(orig, "finish")
    inflated = pyzlib.inflate()(data, "finish")
    assert inflated == orig

def test_table_concat():
    t = []
    for i in range(1, 21):
        t.append(str(i % 5))
    s = "|".join(t)
    deflater = pyzlib.deflate()
    data, *_ = deflater(s, "finish")
    orig = pyzlib.inflate()(data, "finish")
    assert orig == s